import urllib.request
import feedparser
import tarfile
import os
from urllib.parse import urlencode

def download_paper_by_id(arxiv_id, download_dir="downloads"):
    """
    Download source files for a paper using its arXiv ID.
    
    Parameters:
    arxiv_id (str): arXiv ID (e.g., "2311.17667" or "1706.03762")
    download_dir (str): Directory to save downloaded files
    
    Returns:
    str: Path to downloaded files or None if download fails
    """
    # Create download directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)
    
    # Clean the arXiv ID (remove version if present)
    clean_id = arxiv_id.split('v')[0]
    
    # Fetch the paper metadata first to verify it exists
    base_url = 'http://export.arxiv.org/api/query?'
    search_query = urlencode({
        'id_list': clean_id,
    })
    
    response = urllib.request.urlopen(base_url + search_query)
    feed = feedparser.parse(response.read())
    
    if len(feed.entries) == 0:
        print(f"No paper found with ID {arxiv_id}")
        return None
    
    # Get the paper's details
    # paper = feed.entries[0]
    # title = paper.title
    
    # print(f"Found paper: {title}")
    # print(f"arXiv ID: {clean_id}")
    
    # Construct the URL for the source files
    source_url = f'https://arxiv.org/e-print/{clean_id}'
    
    # Download the source files (usually comes as a tar.gz)
    target_file = os.path.join(download_dir, f'{clean_id}.tar.gz')
    # print(f"Downloading source files to {target_file}...")
    
    try:
        urllib.request.urlretrieve(source_url, target_file)
        
        # Extract the tar.gz file
        extract_dir = os.path.join(download_dir, clean_id)
        os.makedirs(extract_dir, exist_ok=True)
        
        with tarfile.open(target_file, 'r:gz') as tar:
            tar.extractall(path=extract_dir)
        
        # Clean up the tar.gz file
        os.remove(target_file)
        
        # print(f"Successfully downloaded and extracted files to {extract_dir}")
        return extract_dir
        
    except Exception as e:
        print(f"Error downloading or extracting files: {str(e)}")
        return None


def get_tex_file(folder_dir):
    '''
    Function that finds a tex file in a given directory and deletes all 
    other non-tex files.
    '''
    tex_files = []
    for root, dirs, files in os.walk(folder_dir):
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))
            else:
                os.remove(os.path.join(root, file))
    if len(tex_files) > 0:
        return tex_files[0]
    
def get_tex_file_path(arxiv_id, download_dir="downloads"):
    '''
    Function that downloads a paper by its arXiv ID and returns the path to the
    main tex file.
    '''
    tex_folder = download_paper_by_id(arxiv_id, download_dir)
    tex_file_path = get_tex_file(tex_folder)
    return tex_file_path

    
# if __name__ == "__main__":
#     arxiv_id = "2410.18611"
#     local_path = r'C:\Users\piotr\Documents\GitHub\mathhack'
#     # tex_file = get_tex_file(arxiv_id, download_dir=local_path)
#     tex_folder = download_paper_by_id(arxiv_id, download_dir=local_path)
#     tex_file_path = get_tex_file(tex_folder)
#     if tex_file_path:
#         print(f"Main TeX file: {tex_file_path}")
#     else:
#         print("Could not find TeX file")
   