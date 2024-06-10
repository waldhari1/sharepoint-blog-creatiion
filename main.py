import pandas as pd
import requests
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
from dotenv import load_dotenv 
import os

load_dotenv()  # Make sure this is at the top of your file

# Debugging: Print out the environment variables to ensure they're being loaded
username = os.getenv('SHAREPOINT_USERNAME')
password = os.getenv('SHAREPOINT_PASSWORD')
print(f"Username: {username}, Password: {password}")

# Step 1: Load the CSV file
file_path = 'Avior Blog Content - Blogs.csv'
blog_posts_df = pd.read_csv(file_path)

# Step 2: Helper function to extract content from the links
import requests

def fetch_blog_content(url):
    """
    Fetches the content of a blog from a given URL.

    Args:
        url (str): The URL of the blog.

    Returns:
        str or None: The content of the blog if the request is successful (status code 200),
                     otherwise None.
    """
    # Send a GET request to the specified URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return the text content of the response
        return response.text
    else:
        # Return None if the request was not successful
        return None

# Step 3: Authenticate to SharePoint
username = os.getenv('SHAREPOINT_USERNAME')
password = os.getenv('SHAREPOINT_PASSWORD')
site_url = os.getenv('SHAREPOINT_SITE_URL')
authcookie = Office365('https://nvcwealth.sharepoint.com/', username=username, password=password).GetCookies()
site = Site(site_url, version=Version.v365, authcookie=authcookie)

# Function to create a new blog post on SharePoint
def create_blog_post(title, content):
    page_name = title.replace(' ', '_') + '.aspx'
    page_data = {
        '__metadata': {'type': 'SP.Publishing.SitePage'},
        'Title': title,
        'CanvasContent1': content,
        'BannerImageUrl': '/sites/yoursite/SiteAssets/default-banner.jpg',
        'Description': '',
        'PromotedState': 1,
        'FirstPublishedDate': '',
        'ContentTypeId': '0x0101009D1CB255DA76424F860D91F20E6C411800B69730500C304AA914EB015F89DCDF1F0063'
    }

    site.Pl.List('SitePages').AddSingleListItem(page_data)

# Step 4: Process each row in the DataFrame
for index, row in blog_posts_df.iterrows():
    title = row['Google Doc']
    link = row['published content link']
    content = fetch_blog_content(link)
    
    if content:
        create_blog_post(title, content)

print("Blog posts have been created successfully!")