# DKU Alibi Project

## Project Overview
<img width="889" alt="Screenshot 2024-06-21 at 5 56 56 PM" src="https://github.com/isu-kim/dku-alibi-embedded/assets/49092508/09a521c5-4503-43a5-8dbb-7baf5c2d4ebb">

### Main Features
- Attendance Check
- Class Engagement Check
- Web UI Interface

## Attendance Check
<img width="662" alt="Screenshot 2024-06-21 at 5 58 18 PM" src="https://github.com/isu-kim/dku-alibi-embedded/assets/49092508/25c9180e-585b-46f9-9cb7-fa10beeea19f">

- Detects user faces and checks who is attending a specific class

## Class Engagement Check
<img width="686" alt="Screenshot 2024-06-21 at 5 58 40 PM" src="https://github.com/isu-kim/dku-alibi-embedded/assets/49092508/6d67d4c2-6c77-444d-ae0d-2b640a8c81d2">

- Detects user faces as well as their concentration rate in the class

## Disclaimers
We have utilized the following opensource projects:
- [YOLO v8](https://github.com/ultralytics/ultralytics): Facial detection, engagement detection

Also, for dataset, please refer to the following document:
- [data.md](./data.md)

## Technologies Used
### ML
- PyTorch
- Dlib

### Cloud
- Docker
- MongoDB

### Frontend, Backend
- Flask
- Django

### Communication
- REST API
- gRPC

## Demo PPT
> Click for Youtube redirect
[![Video Label](http://img.youtube.com/vi/bdYUOdlMKRY/0.jpg)](https://youtu.be/bdYUOdlMKRY)

## LICENSE
The project utilizes a GPL License.

## Team
- [Kim Doik (김도익)](https://github.com/DoIkk) - 32217072: Facial recognition and data labeling
- [Kim Minjung (김민중)](https://github.com/eggplantgf) - 32200584: Engagement detection (sleepiness, yawn) and data labeling
- [Kim Isu (김이수)](https://github.com/isu-kim) - 32190984: Backend, frontend cloud development and data labeling
- [Shokhrukh Talatov](https://github.com/shokhtalat) - 32195077: Engagement detection (eye motion detection) and data labeling

## Contribution
- If you have found bugs, please report them using the issues section.
- For contribution please use PR.
  
