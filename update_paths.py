import os
import re

def update_paths():
    target_dir = r"c:\Users\pc\Desktop\BI\AdventureWorks Cycle - Talend project"
    old_path = r"C:/Users/Morganis/Desktop/BI Final Project DataSet"
    new_path = r"c:/Users/pc/Desktop/BI/Dataset"
    
    # We will also support backslash versions just in case
    old_path_bs = old_path.replace('/', '\\')
    
    count = 0
    print(f"Starting path replacement in directory: {target_dir}")
    print(f"Targeting: {old_path} -> {new_path}")
    
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            # Check only text files to avoid corrupting binaries
            if file.endswith(('.item', '.properties', '.java', '.xml', '.project', '.classpath')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Check if search terms are present
                    has_match = False
                    if old_path in content or old_path_bs in content:
                        has_match = True
                    # Let's also check case-insensitive just in case
                    elif re.search(re.escape(old_path), content, re.IGNORECASE) or re.search(re.escape(old_path_bs), content, re.IGNORECASE):
                        has_match = True
                        
                    if has_match:
                        # Case-insensitive replacement
                        content = re.sub(re.escape(old_path), new_path, content, flags=re.IGNORECASE)
                        content = re.sub(re.escape(old_path_bs), new_path, content, flags=re.IGNORECASE)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Updated: {file_path}")
                        count += 1
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
    print(f"Replacement complete. Total files updated: {count}")

if __name__ == '__main__':
    update_paths()
