# assignment_ParallelDots
Take the loftr inference pipeline from kornia and dockerize and make it ready for deployment. https://kornia.readthedocs.io/en/latest/_modules/kornia/feature/loftr/loftr.html .
The api created should take two images for matching and return a path to an output image that visualizes matching done on both the images side by side.

# Input and Output Storage
media directory contain the output matching images where as media/uploads directory contains input images

# Screenshots
1. API implementation screenshot are available in screenshot directory
2. Additionally it also contains few documentation Screenshots.

# References
1. https://kornia-tutorials.readthedocs.io/en/latest/_nbs/image_matching.html
2. https://kornia.readthedocs.io/
3. https://zju3dv.github.io/loftr/

# Run Server
1. docker build -t image_matching_api .
2. docker run -p 8000:8000 image_matching_api

