import tkinter as tk
from simplepyble import Adapter

window = tk.Tk()
window.title("Bluetooth Scanner")
window.geometry("500x500")

label = tk.Label(window, text="Nearby Devices")
label.pack(pady=10)

device_list = tk.Listbox(window, width=60, height=20)
device_list.pack(pady=10)

def scan_devices():

    device_list.delete(0, tk.END)

    try:
        adapters = Adapter.get_adapters()

        if len(adapters) == 0:
            device_list.insert(tk.END, "No Bluetooth Adapter Found")
            return

        adapter = adapters[0]

        adapter.scan_for(5000)

        results = adapter.scan_get_results()

        if len(results) == 0:
            device_list.insert(tk.END, "No Devices Found")

        for device in results:

            name = device.identifier()

            if name == "":
                name = "Unknown Device"

            device_list.insert(
                tk.END,
                f"{name} - {device.address()}"
            )

    except Exception as e:
        device_list.insert(tk.END, str(e))

scan_button = tk.Button(
    window,
    text="Scan Devices",
    command=scan_devices
)

scan_button.pack(pady=10)

window.mainloop()