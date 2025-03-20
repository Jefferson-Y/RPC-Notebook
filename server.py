from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import threading
import os
import time
import requests

XML_FILE = "db.xml"


def init_xml():
    if not os.path.exists(XML_FILE):
        root = ET.Element("data")
        tree = ET.ElementTree(root)
        tree.write(XML_FILE)


def save_xml(tree):
    tree.write(XML_FILE)


class NotebookServer:
    def add_note(self, topic, note_name, text, timestamp):
        tree = ET.parse(XML_FILE)
        root = tree.getroot()

        topic_element = None
        for t in root.findall("topic"):
            if t.get("name") == topic:
                topic_element = t
                break

        if topic_element is None:
            topic_element = ET.SubElement(root, "topic", name=topic)

        note = ET.SubElement(topic_element, "note", name=note_name)
        ET.SubElement(note, "text").text = text
        ET.SubElement(note, "timestamp").text = timestamp

        save_xml(tree)
        return f"Note '{note_name}' added to topic: {topic}"

    def get_notes(self, topic):
        tree = ET.parse(XML_FILE)
        root = tree.getroot()

        for t in root.findall("topic"):
            if t.get("name") == topic:
                notes = []
                for note in t.findall("note"):
                    note_name = note.get("name", "Untitled")
                    text = note.find("text").text
                    timestamp = note.find("timestamp").text
                    notes.append(f"{note_name}: [{timestamp}] {text}")
                return "\n".join(notes) if notes else "No notes found"
        return "Topic not found"

    def search_wikipedia(self, topic):
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "opensearch",
            "search": topic,
            "limit": 1,
            "namespace": 0,
            "format": "json"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if len(data[3]) > 0:
                wiki_link = data[3][0]

                tree = ET.parse(XML_FILE)
                root = tree.getroot()
                topic_element = None
                for t in root.findall("topic"):
                    if t.get("name") == topic:
                        topic_element = t
                        break

                if topic_element is None:
                    topic_element = ET.SubElement(root, "topic", name=topic)

                note = ET.SubElement(topic_element, "note", name="Wikipedia Info")
                ET.SubElement(note, "text").text = f"Wikipedia page: {wiki_link}"
                ET.SubElement(note, "timestamp").text = time.strftime("%Y-%m-%d %H:%M:%S")
                save_xml(tree)

                return f"Wikipedia page added to topic '{topic}': {wiki_link}"
            return "No Wikipedia content found"
        except requests.exceptions.RequestException as e:
            return f"Wikipedia request failed: {e}"


def run_server():
    init_xml()
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    server.register_instance(NotebookServer())
    print("Server started, waiting for client connections...")
    server.serve_forever()


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()