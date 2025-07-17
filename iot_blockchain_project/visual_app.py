import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import datetime
import time
import random
import json

from simulation.metrics import Metrics
from simulation.network_simulator import NetworkSimulator
from blockchain_layer.blockchain import Blockchain
from blockchain_layer.block import Block


class IoTBlockchainVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title('IoT Blockchain Network Visualizer')
        self.root.geometry('1000x700')

        self.metrics = Metrics()
        self.simulator = NetworkSimulator()
        self.blockchain = Blockchain()

        self.setup_ui()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)

        self.blockchain_tab = ttk.Frame(self.notebook)
        self.network_tab = ttk.Frame(self.notebook)
        self.metrics_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.blockchain_tab, text='Blockchain')
        self.notebook.add(self.network_tab, text='Network')
        self.notebook.add(self.metrics_tab, text='Metrics')
        self.notebook.pack(expand=1, fill='both', padx=10, pady=10)

        self.setup_blockchain_tab()
        self.setup_network_tab()
        self.setup_metrics_tab()

    def setup_blockchain_tab(self):
        columns = ('index', 'timestamp', 'data', 'previous_hash', 'hash')
        self.tree = ttk.Treeview(self.blockchain_tab, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col.capitalize().replace('_', ' '))
            self.tree.column(col, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        add_block_btn = tk.Button(
            self.blockchain_tab,
            text='Add Block',
            command=self.add_block,
            bg='#4CAF50',
            fg='white',
            padx=10,
            pady=5
        )
        add_block_btn.pack(pady=10)

        self.refresh_blockchain_table()

    def setup_network_tab(self):
        self.network_fig, self.network_ax = plt.subplots(figsize=(6, 4))
        self.network_canvas = FigureCanvasTkAgg(self.network_fig, master=self.network_tab)
        self.network_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.network_status = tk.Label(self.network_tab, text='', fg='blue')
        self.network_status.pack(pady=5)

        simulate_btn = tk.Button(
            self.network_tab,
            text='Simulate Message',
            command=self.simulate_message,
            bg='#2196F3',
            fg='white',
            padx=10,
            pady=5
        )
        simulate_btn.pack(pady=5)

        self.update_network_tab()

    def setup_metrics_tab(self):
        self.metrics_fig, self.metrics_ax = plt.subplots(figsize=(6, 4))
        self.metrics_canvas = FigureCanvasTkAgg(self.metrics_fig, master=self.metrics_tab)
        self.metrics_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        show_all_btn = tk.Button(
            self.metrics_tab,
            text='Show All Simulation Data',
            command=self.show_all_simulation_data,
            bg='#FF9800',
            fg='white',
            padx=10,
            pady=5
        )
        show_all_btn.pack(pady=10)

        self.update_metrics_chart()

    def add_block(self):
        try:
            data = {
                "device_id": f"sensor_{random.randint(1, 5)}",
                "value": round(random.uniform(20, 30), 2),
                "type": "temperature",
                "timestamp": time.time()
            }
            data_json = json.dumps(data)
            # Pick a validator (for demo, just use validator1)
            validator_id = "validator1"
            self.blockchain.add_block(data_json, validator_id)
            self.refresh_blockchain_table()
            self.update_network_tab()
            self.update_metrics_chart()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add block: {str(e)}")

    def refresh_blockchain_table(self):
        self.tree.delete(*self.tree.get_children())
        for block in self.blockchain.get_chain():
            self.tree.insert('', tk.END, values=(
                block['index'],
                datetime.datetime.fromtimestamp(block['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                str(block['data'])[:30] + '...' if len(str(block['data'])) > 30 else str(block['data']),
                block['previous_hash'][:8] + '...',
                block['hash'][:8] + '...'
            ))

    def simulate_message(self):
        chain = self.blockchain.get_chain()
        if len(chain) < 2:
            self.network_status.config(text="Add more blocks to simulate messages.")
            return

        nodes = [f"Block{block['index']}" for block in chain]
        src, dst = random.sample(nodes, 2)

        latency = self.simulator.send_message(src, dst, 'msg')
        power = random.uniform(0.1, 1.0)

        self.metrics.record_latency(latency)
        self.metrics.record_power(power)

        self.network_status.config(
            text=f'{src} → {dst} | Latency: {latency*1000:.1f} ms | Power: {power:.2f} W'
        )
        self.update_metrics_chart()

    def update_network_tab(self):
        self.network_ax.clear()
        chain = self.blockchain.get_chain()
        G = nx.Graph()

        nodes = [f"Block{block['index']}" for block in chain]
        G.add_nodes_from(nodes)

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                G.add_edge(nodes[i], nodes[j])

        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', ax=self.network_ax)
        self.network_ax.set_title("Blockchain P2P Node Network")
        self.network_canvas.draw()

    def update_metrics_chart(self):
        self.metrics_ax.clear()
        latencies = self.simulator.latencies

        if latencies:
            self.metrics_ax.plot(
                [i + 1 for i in range(len(latencies))],
                [l * 1000 for l in latencies],
                marker='o',
                color='green'
            )
            self.metrics_ax.set_title('Latency Between Blockchain Nodes')
            self.metrics_ax.set_xlabel('Message Count')
            self.metrics_ax.set_ylabel('Latency (ms)')
        else:
            self.metrics_ax.text(0.5, 0.5, 'No data yet', ha='center', va='center')

        avg_latency = self.metrics.get_average_latency() * 1000
        avg_power = self.metrics.get_average_power()
        self.metrics_ax.text(0.05, 0.95, f'Avg Latency: {avg_latency:.2f} ms', transform=self.metrics_ax.transAxes)
        self.metrics_ax.text(0.05, 0.90, f'Avg Power: {avg_power:.2f} W', transform=self.metrics_ax.transAxes)

        self.metrics_canvas.draw()

    def show_all_simulation_data(self):
        # Gather all simulation data
        blocks = self.blockchain.get_chain()
        latencies = self.simulator.latencies
        powers = self.metrics.power_consumptions

        blocks_str = "\n".join([
            f"Block {b['index']}: {b['data']}" for b in blocks
        ])
        latencies_str = ", ".join([f"{l*1000:.2f}ms" for l in latencies])
        powers_str = ", ".join([f"{p:.2f}W" for p in powers])

        msg = (
            f"Blocks:\n{blocks_str}\n\n"
            f"Latencies:\n{latencies_str}\n\n"
            f"Power Consumptions:\n{powers_str}"
        )
        messagebox.showinfo("All Simulation Data", msg)


if __name__ == '__main__':
    root = tk.Tk()
    app = IoTBlockchainVisualizer(root)
    root.mainloop()
