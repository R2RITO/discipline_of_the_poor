# Image upload

To upload images, a couple of steps are needed, mainly configuration ones,
because django takes care of the multipart form and the data type conversions

### Storage

The image is stored on disk instead of the database, and the field in the
database is a path to the file in disk (not an absolute path).

To determine the upload path, a dedicated folder is created, and then
a folder for each user, along with the uploaded file with its timestamp
appended.

To configure it, set the variables:

    # Media handling

    MEDIA_ROOT = os.environ.get('BASE_MEDIA_ROOT')
    MEDIA_URL = os.environ.get('MEDIA_URL')
    BUDGET_MEDIA_FOLDER = os.environ.get('BUDGET_MEDIA_FOLDER')

### Serving

After the file is stored, the list resources show the MEDIA_URL + the
stored path of the file. To serve it to the users, a web server must be set up.

##### Nginx

To use nginx, after installing it, configure a new site for this project by
creating the file:

    /etc/nginx/sites-enabled/dotp
    
With contents as such:

    server {
        server_name localhost;
        listen 127.0.0.1:80;
        listen 10.0.0.207:80;
    
        location /budget_media/ {
            root /home/fulanito/Projects/dotp_media;
        }
            
    } 

And then activate it by creating a symlink:

    ln -s /etc/nginx/sites-available/dotp /etc/nginx/sites-enabled/dotp
    
Restart the server and you should be able to access the file:

    sudo service nginx restart