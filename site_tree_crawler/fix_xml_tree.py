import xml.etree.ElementTree as ET
from xml.dom import minidom
from urllib.parse import urlparse
import sys
import os

def fix_xml_structure(input_file, output_file=None):
    if not os.path.exists(input_file):
        print(f"❌ Файл не знайдено: {input_file}")
        return

    print(f"Reading {input_file}...")
    tree = ET.parse(input_file)
    root = tree.getroot()
    
    root_url = root.attrib.get("root")
    if not root_url:
        print("Error: Could not find 'root' attribute in XML root element.")
        return

    # Збираємо всі унікальні URL з файлу
    all_urls = set()
    all_urls.add(root_url)
    for page in root.iter("page"):
        url = page.attrib.get("url")
        if url:
            # Очищуємо від параметрів та фрагментів
            clean_url = url.split('?')[0].split('#')[0]
            all_urls.add(clean_url)

    print(f"Found {len(all_urls)} unique URLs. Building new structure...")

    # Логіка побудови дерева (ідентична тій, що в павуку)
    parsed_root = urlparse(root_url)
    root_base = f"{parsed_root.scheme}://{parsed_root.netloc}{parsed_root.path}"
    if not root_base.endswith('/'):
        root_base += '/'

    new_tree_data = {"_url": root_url, "children": {}}

    def add_to_tree(url):
        if url == root_url or url == root_base.rstrip('/'):
            return
        
        if not url.startswith(root_base):
            return
        
        rel_path = url[len(root_base):].strip('/')
        if not rel_path:
            return
            
        segments = rel_path.split('/')
        current_node = new_tree_data["children"]
        
        path_so_far = root_base
        for i, seg in enumerate(segments):
            path_so_far += seg
            if i < len(segments) - 1 or url.endswith('/'):
                path_so_far += '/'
            
            if seg not in current_node:
                current_node[seg] = {"_url": path_so_far if i < len(segments) - 1 else url, "children": {}}
            current_node = current_node[seg]["children"]

    for url in sorted(all_urls):
        add_to_tree(url)

    # Генерація нового XML
    new_root_elem = ET.Element("site_tree", {"root": root_url})

    def build_xml_recursive(node_data, parent_elem):
        for segment in sorted(node_data.keys()):
            item = node_data[segment]
            page_elem = ET.SubElement(parent_elem, "page", {"url": item["_url"], "segment": segment})
            if item["children"]:
                build_xml_recursive(item["children"], page_elem)

    build_xml_recursive(new_tree_data["children"], new_root_elem)

    xml_str = ET.tostring(new_root_elem, encoding="unicode")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")

    if not output_file:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_fixed{ext}"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"Done! New file saved: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Використання: python fix_xml_tree.py <шлях_до_xml_файлу>")
    else:
        fix_xml_structure(sys.argv[1])
