# Stock-Tracking-Application

## Overview
This Python application utilizes the Tkinter library to create a graphical user interface for tracking real-time stock market data. It fetches stock information from the "api.collectapi.com" API, allowing users to monitor selected stocks, view profit/loss, and analyze their portfolio.

## Features
**User-Friendly Interface:** The application provides an intuitive interface with buttons, comboboxes, and entry fields for easy interaction.

**Live Stock Data:** Real-time stock market data is fetched from the API, including stock symbols, prices, and other relevant information.

**Dynamic Table:** The main table dynamically updates to display stock name, price, quantity, profit/loss, and total amount. Users can sort the table by clicking on column headers.

**Threading:** The application uses threading to run the stock tracking function concurrently, ensuring a responsive GUI.

**Visualization:** A summary window displays the total amount and profit/loss, accompanied by a pie chart created using the Matplotlib library.

## Prerequisites
API Key from "api.collectapi.com"

Matplotlib Library

Tkinter Library

Requests Library 
