# Spotify Data Analysis Project

I'm building my own version of Spotify Wrapped, available year round. 

## Features

- **Main Page**: See index.html for code, this page routes to see different metrics for your streaming data. 

- **Songs, Genres, and Artists**: See different trends and grpahics for your spotify data. 

## Technologies Used

- **Flask**: Web framework used to serve the web pages.
- **HTML**: For the structure of the web pages.
- **CSS**: For styling the pages and buttons.
- **JavaScript**: To dynamically enable buttons based on name selection and set correct links.

## How to Run

1. **Clone the repository**:
    ```bash
    git clone <repo_url>
    cd spotify
    ```

2. **Build the Docker container**:
    ```bash
    make
    ```

3. **Access the app**:
    Open your browser and go to `http://localhost:5000`.


4. **Clean up**
    Press Control+C to interupt terminal, then type 

    '''bash 
    make clean
    '''
    

