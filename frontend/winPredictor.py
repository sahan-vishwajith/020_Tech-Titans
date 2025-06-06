import streamlit as st
import base64
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode() 

def set_background(image_file):
    base64_image = get_base64(image_file)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-size: 100% 100%;  
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

def create_circle_image(image, size):
    try:
        # Create a circular mask
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)

        # Resize image
        image = image.resize((size, size))

        # Apply circular mask
        image = Image.composite(image, Image.new('RGBA', image.size), mask)
        return image
    except Exception as e:
        print(f"Error creating circle image: {e}")
        return Image.new('RGBA', (size, size))  # Return a blank image in case of error

def create_chart():
    # Fixed size for all images
    fixed_size = 50  # Example size in pixels

    # Load and prepare candidate images
    image_path1 = './photos/sajith.jpeg'
    image_path2 = './photos/anura.jpeg'
    image_path3 = './photos/namal.jpeg'
    image_path4 = './photos/ranil.jpeg'
    images = {
        'Sajith Premadasa': create_circle_image(Image.open(image_path1), fixed_size),
        'Anura Kumara Dissanayake': create_circle_image(Image.open(image_path2), fixed_size),
        'Ranil Wickremesinghe': create_circle_image(Image.open(image_path4), fixed_size),
        'Namal Rajapakshe': create_circle_image(Image.open(image_path3), fixed_size)
    }

    # Data
    candidates = ['Namal Rajapakshe', 'Sajith Premadasa', 'Anura Kumara Dissanayake', 'Ranil Wickremesinghe']
    votes = [7, 37, 41, 15]
    colors = ['purple', 'orange', 'red', 'green']

    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(14, 6))  # Increase figure width to accommodate images
    
    # Set transparent background to match dark mode
    fig.patch.set_facecolor('none')  # Remove white background
    ax.set_facecolor('none')         # Set ax background to transparent
    
    bars = ax.barh(candidates, votes, color=colors, height=0.5)  # Adjust bar height to make space for images

    # Add the percentage labels on the bars
    for bar, vote in zip(bars, votes):
        # Display percentage within the bar
        plt.text(bar.get_width() - 2, bar.get_y() + bar.get_height()/2, f'{vote}%',
                va='center', ha='center', color='white', fontsize=25, fontweight='bold')

    # Add candidate images to the end of each bar
    for i, candidate in enumerate(candidates):
        bar_width = bars[i].get_width()
        # Set the position for the image
        imagebox = OffsetImage(images[candidate], zoom=fixed_size / 60)  # Adjust zoom based on fixed size
        ab = AnnotationBbox(
            imagebox, 
            (bar_width +1, i),  # Increase spacing to avoid overlap
            frameon=False, 
            box_alignment=(0, 0.5)  # Align image so it's centered vertically with the bar
        )
        ax.add_artist(ab)

    # Extend the x-axis limits to accommodate images
    ax.set_xlim(0, max(votes) + fixed_size * 0.1)  # Extend x-axis limit by image size

    # Remove right y-axis and bottom x-axis
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_linewidth(0.5)  # Optional: make the remaining spines thinner
    ax.spines['top'].set_visible(False)   # Optional: make the remaining spines thinner

    # Hide x-axis tick labels
    ax.set_xticks([])

    # Set y-axis label font size
    ax.tick_params(axis='y', which='major', labelsize=23, pad=10, colors='white')

    # Use Streamlit to display the chart
    st.pyplot(fig)

def winPredictor():
    st.title("Win Prediction")

    # Display chart
    create_chart()

        
        
        
