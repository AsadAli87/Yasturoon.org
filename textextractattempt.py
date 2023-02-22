import os
import re
import PyPDF2
import traceback

def extract_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(open(pdf_path, 'rb'))
        text = ''
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text() + '\n'
        return text, pdf_reader


def categorize_text(text):
    if text is None or text.strip() == '':
        return []
    items = []
    current_item = {'title': '', 'text': ''}
    title_lines = []
    for line in text.split('\n'):
        if line.isupper() or len(line) < 3:
            if title_lines:
                current_item = {'title': ' '.join(title_lines), 'text': ''}
                title_lines = []
                items.append(current_item)
            else:
                if current_item['title'] and current_item['text']:
                    items.append(current_item)
                title = line[:30] if len(line) > 30 else line
                current_item = {'title': title, 'text': ''}
        else:
            title_lines.append(line)
            current_item['text'] += line + '\n'
    if title_lines or (current_item['title'] and current_item['text']):
        items.append(current_item)
    return items

def generate_output_files(items, output_dir, file):
    file_without_extension = os.path.splitext(file)[0]
    current_output_dir = os.path.join(output_dir, file_without_extension)
    if not os.path.exists(current_output_dir):
        os.makedirs(current_output_dir)
    for item in items:
        filename = item['title'].replace(' ', '_').replace('*', '-').replace(':', '-').replace('/', '-').replace('\\', '-').replace('__', '')
        filename = re.sub(r'[^\w\s-]', '', filename) # Remove all characters that are not letters, numbers, spaces, or hyphens
        with open(os.path.join(current_output_dir, f'{filename}.txt'), 'w', encoding='utf-8') as file:
            file.write(item['text'].replace("/x00", ""))            

if __name__ == '__main__':
    pdf_folder = 'C:/Users/Asad Ali/Desktop/Yasturoon.org/Reference Materials used throughout the process/Text Analysis Sample/'
    output_dir = 'C:/Users/Asad Ali/Desktop/Yasturoon.org/Reference Materials used throughout the process/Text Analysis Sample/Text Extracts/'
    for file in os.listdir(pdf_folder):
        pdf_path = os.path.join(pdf_folder, file)
        try:
            text, pdf_reader = extract_text(pdf_path)
            print(f"Extracted text from {file}: {text[:100]}...")
            items = categorize_text(text)
            print(f"Categorized items from {file}: {items}")
            generate_output_files(items, output_dir, file)
            print(f"Output file for {file} generated.")
        except Exception as e:
            print(f"Problem encountered during process for {file}: {e}")
            print(traceback.print_exc())
