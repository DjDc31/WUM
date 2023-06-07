# WUM - Web Usage Monitor

Monitor and display your internet usage in real-time using this Python script based on psutil and curses.

## Introduction

Web Usage Monitor is a Python script that allows you to monitor and display your internet usage in real-time. It provides information on the amount of data sent and received since Wi-Fi activation, helping you keep track of your network usage.

The script is particularly useful for individuals working remotely and relying on their phone's tethering functionality for internet access. It enables you to monitor your data usage while connected to your phone's shared connection, ensuring you stay within your data plan limits.

The script uses the psutil library to retrieve network statistics and the curses library to create a text-based user interface. By running the script, you can see the data sent and received since Wi-Fi activation in gigabytes (GB).

<img src="https://i.ibb.co/2NGChB5/Capture-d-cran-2023-06-07-19-07-14.png" alt="How it works" />

## Features

- Real-time monitoring of internet usage
- Display of data sent and received since Wi-Fi activation
- Ideal for telecommuters relying on phone tethering
- Simple and intuitive text-based interface
- Option to reset usage to zero with the press of a button

## Prerequisites
- Python 3.x installed on your computer [Python](https://www.python.org/downloads/)
- psutil library installed, can be installed via:
   ```shell
   pip install psutil
   ```

## How to Use 🧑‍💻

1. Clone this repository to your local machine:
   ```shell
   git clone https://github.com/DjDc31/WUM.git
   ```

2. Navigate to the project directory:
   ```shell
   cd WUM
   ```

3. Run the main script:
   ```shell
   python main.py
   ```

4. The script will display the web usage statistics, including data sent and received since Wi-Fi activation, in gigabytes (GB).

5. To reset the usage to zero, press the 'R' key.

6. Enjoy monitoring your internet usage with Web Usage Monitor!


## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository.

## Acknowledgments

Special thanks to the developers of psutil and curses for their excellent libraries that made this project possible.

## Support

If you find this project helpful, please consider giving it a star on GitHub. Your support is greatly appreciated!⭐️

