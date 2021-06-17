# Audio_processing
<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Polina418/Audio_processing">
    <img src="/logo2.png" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">Speech processing tool (SPONGE)</h3>

  <p align="center">
    Script for audio processing - smoothing data, speech recognition, speech onset detection.
    This script might not work for you if you need to further extract any lingustic futures! Be careful.
    <br />
    <a href="https://github.com/Polina418/Audio_processing"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Polina418/Audio_processing">View Demo</a>
    ·
    <a href="https://github.com/Polina418/Audio_processing/issues">Report Bug</a>
    ·
    <a href="https://github.com/Polina418/Audio_processing/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

There are many great softwares to analyze your audio recordings from your participants, however, I didn't find one that really suit my needs so I created this enhanced one. I want to create a software that will help you deal with your data as fast and as accurate as possible. Why should you try this software?

Here's why:
* Your time should be focused on creating new experiments, improving science, not manual processing of your files. 
* You shouldn't be doing the same tasks over and over like cleaning the files, manually detecting onsets, recording the responses.

Of course, no one software will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. Thanks to all the people who have contributed to expanding this software!

A list of commonly used resources that I find helpful are listed in the acknowledgements.

### Built With

This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [Python](https://https://www.python.org/)
* [Spyder](https://www.spyder-ide.org/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites
Here is a list of Python libraries you´ll need to install in order to work with the software
- subprocess 
- librosa==0.8.0
- pandas==1.0.3
- numpy==1.17.5
- scipy==1.3.3
- matplotlib==3.1.3
- playsound==1.2.2
- google-cloud==0.34.0
- google-cloud-speech==2.3.0
- re
- from io audioread==2.1.9, SpeechRecognition==3.8.1, wavio==0.0.4
- jinja2-time==0.2.0
- os
- IPython
- glob==0.7

Example of installation on a Windows machine pip install 'PackageName==1.4'
It is a good practice to create a virtual environment and install all the packages needed for a particular project to avoid interference from other versions. Read more: https://docs.python.org/3/library/venv.html

### Installation

1. If you want to use Speech Recognition, you need to get an API key, save it in your projects' folder and add the path to the file to environmental variables on your computer.
2. Clone the repository using git or manually
   ```sh
   git clone https://github.com/Polina418/Audio_processing/
   ```
3. Create and activate your virtual envirenment 
   ```sh
   python3 -m venv /path/to/new/virtual/environment
   ```
4. Install python packages
   ```sh
   pip install ...
   ```


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- CONTACT -->
## Contact

Timofeeva Polina - [@PolinaT74054073](https://twitter.com/PolinaT74054073) - timofeeva.polina.serg@gmail.com

Project Link: [https://github.com/Polina418/Audio_processing](https://github.com/Polina418/Audio_processing)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Animate.css](https://daneden.github.io/animate.css)
* [Loaders.css](https://connoratherton.com/loaders)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
* [Sticky Kit](http://leafo.net/sticky-kit)
* [JVectorMap](http://jvectormap.com)
* [Font Awesome](https://fontawesome.com)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/Polina418/Audio_processing/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/Polina418/Audio_processing/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/Polina418/Audio_processing/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/Polina418/Audio_processing/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/Polina418/Audio_processing/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/polina-timofeeva-70b996177/
[product-screenshot]: images/screenshot.png
