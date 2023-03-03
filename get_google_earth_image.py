from urllib import request, parse
import webbrowser

# Might want to use Google Maps Static API
# https://developers.google.com/maps/documentation/maps-static/overview
# https://developers.google.com/maps/get-started

def get_google_earth_img(location, zoom=15, size=(640, 640), file_path='results\\output.jpg'):
    encoded_location = parse.quote(location)
    # Construct the Google Earth URL for the specified location
    url = f"https://www.google.com/maps/@?api=1&map_action=map&center={encoded_location}&zoom={zoom}&size={size[0]}x{size[1]}&output=embed"

    # Open the URL and retrieve the image data
    with request.urlopen(url) as response:
        image_data = response.read()
    print(image_data)
    try:
        with open(file_path, "wb") as image_file:
            image_file.write(image_data)

        # Debugging: save the image data to a file manually
        with open("image_data.png", "wb") as image_file:
            image_file.write(image_data)
    except Exception as e:
        print(f"Error saving image to file: {e}")
        return

    # Open the image in the default image viewer
    webbrowser.open(file_path)

if __name__ == '__main__':
    get_google_earth_img("1600 Amphitheatre Parkway, Mountain View, CA", file_path='results\\output.jpg')