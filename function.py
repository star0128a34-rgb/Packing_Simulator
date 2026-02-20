# %%
import pandas as pd
import numpy as np

from py3dbp import Packer, Bin, Item, Painter

import seaborn as sns

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# %%
def prepare_boxes(data):
    data['VOLUME'] = data['WIDTH'] * data['HEIGHT'] * data['DEPTH']
    data = data.sort_values(by = ['WEIGHT', 'VOLUME', 'HEIGHT'], ascending = [False, False, False])

    items = []

    palette = sns.color_palette('husl').as_hex()

    for i, box in data.iterrows():
        for n in range(box['QUANTITY']):
            item = Item(partno = f"{box['ID']}_{n + 1}",
                        name = box['ID'],
                        typeof = 'cube',
                        WHD = (box['WIDTH'], box['HEIGHT'], box['DEPTH']),
                        weight = box['WEIGHT'],
                        level = 1,
                        loadbear = 1000,
                        updown = False,
                        color = palette[i])
                        
            items.append(item)

    return items

# %%
def pack_boxes(boxes, pallet_w, pallet_h, pallet_d, pallet_m, pallet_n = 10):
    final_packer = Packer()
    
    unfitted_boxes = boxes

    for n in range(pallet_n):
        if not unfitted_boxes:
            break

        packer = Packer()

        pallet = Bin(partno = f'Pallet_{n + 1}',
                     WHD = (pallet_w, pallet_h, pallet_d),
                     max_weight = pallet_m,
                     corner = 0,
                     put_type = 0)
        
        packer.addBin(pallet)

        for box in unfitted_boxes:
            packer.addItem(box)

        packer.pack(bigger_first = True,
                    fix_point = True,
                    distribute_items = True,
                    check_stable = True,
                    support_surface_ratio = 0.8,
                    number_of_decimals = 0)

        loaded_pallet = packer.bins[0]

        final_packer.addBin(loaded_pallet)

        unfitted_boxes = loaded_pallet.unfitted_items

    return final_packer

def get_data(pallet_bin, pallet_w, pallet_h, pallet_d):
    pallet_volume = pallet_w * pallet_h * pallet_d

    total_volume = 0.0
    total_count = {}

    for item in pallet_bin.items:
        name = item.name
        volume = item.width * item.height * item.depth

        if name not in total_count:
            total_count[name] = 0

        total_volume += float(volume)
        total_count[name] += 1

    remaining_volume = pallet_volume - total_volume

    return [total_count, total_volume, remaining_volume]

# %%
def create_box(x, y, z, w, d, h, color, name, show_legend):
    v = [(x, y, z), (x + w, y, z), (x + w, y + d, z), (x, y + d, z),
         (x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)]

    mx, my, mz = zip(*v)
    
    mesh = go.Mesh3d(x = mx, y = my, z = mz,
                     i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                     j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                     k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                     opacity = 0.9,
                     color = color,
                     flatshading = True,
                     name = name,
                     legendgroup = name,
                     showlegend = show_legend)
    
    ev = [v[0], v[1], v[2], v[3], v[0], None,
          v[4], v[5], v[6], v[7], v[4], None,
          v[0], v[4], None, v[1], v[5], None,
          v[2], v[6], None, v[3], v[7]]
    
    ex, ey, ez = zip(*[p if p else (None, None, None) for p in ev])
    
    edge = go.Scatter3d(x = ex, y = ey, z = ez,
                        mode = 'lines',
                        line = dict(color = 'black', width = 3),
                        showlegend = False,
                        hoverinfo = 'skip')
    
    return [mesh, edge]

# %%
def plot_pallet(pallet_bin, pallet_w, pallet_h):
    fig = go.Figure()
    legend = set()

    for item in pallet_bin.items:
        x, y, z = [float(i) for i in item.position]
        w, d, h = [float(i) for i in item.getDimension()]
        name = item.name

        show_legend = name not in legend

        if show_legend:
            legend.add(name)

        mesh, edge = create_box(x, y, z, w, d, h, item.color, name, show_legend)

        fig.add_trace(mesh)
        fig.add_trace(edge)

    fig.add_trace(go.Mesh3d(x = [0, pallet_w, pallet_w, 0, 0, pallet_w, pallet_w, 0],
                            y = [0, 0, pallet_h, pallet_h, 0, 0, pallet_h, pallet_h],
                            z = [-1, -1, -1, -1, 0, 0, 0, 0],
                            color = 'lightgrey',
                            opacity = 0.3,
                            showlegend = False))

    fig.update_layout(height = 700,
                      margin = dict(l = 0, r = 0, b = 0, t = 40),
                      scene = dict(aspectmode = 'data'))
    
    return fig


