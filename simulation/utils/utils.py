import os
import datetime
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import yaml


CWD = os.getcwd()
CONFIG_PATH = os.path.join(CWD, r'simulation\config\run.yaml')
OUT_PATH = os.path.join(CWD, r'out')


def load_yaml(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)


def save_plot(simulation_config, model_config, simu, show_plot=False):
    date_str = datetime.datetime.now().strftime("%d-%m-%Y")
    folder_name = f"out/{date_str}"

    os.makedirs(folder_name, exist_ok=True)

    time_str = datetime.datetime.now().strftime("%H-%M-%S")
    image_file_path = os.path.join(folder_name, f"{time_str}.png")
    pdf_path = os.path.join(folder_name, f"{time_str}.pdf")

    plot_simulation(simu, image_file_path, show_plot)

    add_configuration_text(pdf_path, simulation_config, model_config, image_file_path)

    os.remove(image_file_path)

    print(f"PDF saved to: {pdf_path}")


def plot_simulation(simu, image_file_path, show_plot):
    plt.figure(figsize=(10, 6))

    iterations = np.arange(len(simu))
    plt.plot(iterations, simu, label="Simulation", color='blue', marker='o')

    spline = UnivariateSpline(iterations, simu, s=0.5)
    x_spline = np.linspace(0, len(simu) - 1, 100)
    y_spline = spline(x_spline)

    plt.plot(x_spline, y_spline, label="Estimation (Spline)", color='orange')

    plt.title("Percentage of Infected During Each Iteration")
    plt.xlabel("Iterations (su)")
    plt.ylabel("Number of Infected (%)")
    plt.ylim(0, 1)
    plt.legend()

    plt.savefig(image_file_path, format='png')

    if show_plot:
        plt.show()

    plt.close()


def add_configuration_text(pdf_path, simulation_config, model_config, image_file_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    image_height = 3 * inch
    c.drawImage(image_file_path, 0.5 * inch, height - image_height - 50, width=7 * inch, height=image_height)

    config_text = f"Network Configuration:\n{simulation_config}\n\nModel Configuration:\n{model_config}"

    text_object = c.beginText(50, height - image_height - 100)
    text_object.setFont("Helvetica", 10)

    for line in config_text.splitlines():
        text_object.textLine(line)

    c.drawText(text_object)
    c.showPage()
    c.save()
