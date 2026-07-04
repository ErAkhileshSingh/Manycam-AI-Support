import os
import re

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def load_documents():
    """Reads all markdown files in data/ and splits them into searchable chunks (sections)."""
    documents = []
    
    if not os.path.exists(DATA_DIR):
        return documents
        
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, DATA_DIR)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Split the document by headings to create smaller chunks
                    sections = re.split(r'\n(##+ .*)\n', content)
                    current_header = file.replace('.md', '').replace('_', ' ').title()
                    
                    # Store the introductory section (before the first subheading)
                    if sections and sections[0].strip():
                        documents.append({
                            'source': rel_path,
                            'title': current_header,
                            'content': sections[0].strip()
                        })
                        
                    # Store subsequent sections
                    for i in range(1, len(sections), 2):
                        if i + 1 < len(sections):
                            sub_header = sections[i].replace('#', '').strip()
                            sec_content = sections[i+1].strip()
                            documents.append({
                                'source': rel_path,
                                'title': f"{current_header} > {sub_header}",
                                'content': sec_content
                            })
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    
    return documents

def search_knowledge_base(query, limit=5):
    """Searches the document chunks using a simple keyword overlap scoring algorithm."""
    if not query:
        return []
        
    query_words = set(re.findall(r'\w+', query.lower()))
    if not query_words:
        return []
        
    docs = load_documents()
    results = []
    
    for doc in docs:
        title_lower = doc['title'].lower()
        content_lower = doc['content'].lower()
        
        # Calculate scoring: higher weight to words in title
        score = 0
        for word in query_words:
            if word in title_lower:
                score += 5  # Title match weight
            if word in content_lower:
                score += content_lower.count(word)
                
        if score > 0:
            results.append({
                'source': doc['source'],
                'title': doc['title'],
                'content': doc['content'],
                'score': score
            })
            
    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:limit]

def get_faqs_list():
    """Parses faqs.md to return a list of FAQ questions and answers for display."""
    faqs = []
    faq_file = os.path.join(DATA_DIR, "faqs", "faqs.md")
    if not os.path.exists(faq_file):
        return faqs
        
    try:
        with open(faq_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse Q&A sections
        qa_blocks = re.findall(r'## (Q\d+:.*?)\n\*\*Answer:\*\* (.*?)(?=\n## |\Z)', content, re.DOTALL)
        for q, a in qa_blocks:
            faqs.append({
                'question': q.strip(),
                'answer': a.strip()
            })
    except Exception as e:
        print(f"Error loading FAQs: {e}")
        
    return faqs
