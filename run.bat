set absolute_path=C:/Users/Tamara/Projects/bsvp/bsvp-csv-export/

docker build -t bsvp-csv-export-development .
docker run^
  -v %absolute_path%data:/code/data:ro^
  -v %absolute_path%configs:/code/configs:ro^
  -v %absolute_path%mappings:/code/mappings:ro^
  -v %absolute_path%export:/code/export^
  -v %absolute_path%logs:/code/logs^
  -p 0.0.0.0:3000:3000^
  -p 0.0.0.0:5000:5000^
  bsvp-csv-export-development npm start
