#!/usr/bin/env python
# coding: utf-8

# # Generate Sankey Plot for KG-COVID-19

# In[1]:


import json
import yaml
import wget
import plotly.graph_objects as go


# In[2]:


def generate_sankey_json_s2c(stats, **kwargs):
    """
    Sankey where col1 is source and col2 is category.
    """
    sankey = json.load(open('sankey_sample.json'))
    sankey_nodes = sankey['data'][0]['node']
    sankey_nodes['label'] = []
    sankey_nodes['x'] = []
    sankey_nodes['y'] = []
    sankey_links = sankey['data'][0]['link']
    sankey_links = {
        'source': [],
        'target': [],
        'label': [],
        'value': [],
        'color': sankey_links['color'],
    }
    sankey['layout']['title']['text'] = f"Sankey Plot for KG-COVID-19"
    all_nodes = ['unknown']
    all_nodes += sorted([x for x in stats['node_stats']['node_categories']])
    all_nodes += sorted(stats['node_stats']['provided_by'])

    fixed = set([x.split(' ')[0] if 'SciBite' in x else x for x in all_nodes])
    all_proper_nodes = sorted(list(fixed))
    sankey_nodes['label'] = all_proper_nodes

    for category_key in stats['node_stats']['count_by_category']:
        target = all_proper_nodes.index(category_key)
        if 'provided_by' in stats['node_stats']['count_by_category'][category_key]:
            for provided_by_key in stats['node_stats']['count_by_category'][category_key]['provided_by']:
                source = all_proper_nodes.index(provided_by_key)
                sankey_links['source'].append(source)
                sankey_links['target'].append(target)
                sankey_links['value'].append(stats['node_stats']['count_by_category'][category_key]['provided_by'][provided_by_key]['count'])
                sankey_links['label'].append(str(stats['node_stats']['count_by_category'][category_key]['provided_by'][provided_by_key]['count']))

    sankey['data'][0]['link'] = sankey_links
    return sankey

def generate_sankey_json_c2c2s(stats):
    """
    Sankey where col1 is category, col2 is category, and col3 is source
    """
    sankey = json.load(open('sankey_sample.json'))
    sankey_nodes = sankey['data'][0]['node']
    sankey_nodes['color'] = sankey_nodes['color'] * 2
    sankey_nodes['label'] = []
    sankey_nodes['x'] = []
    sankey_nodes['y'] = []
    sankey_links = sankey['data'][0]['link']
    sankey_links = {
        'source': [],
        'target': [],
        'label': [],
        'value': [],
        'color': sankey_links['color'] * 2,
    }
    sankey['layout']['title']['text'] = f"Sankey Plot for KG-COVID-19"
    all_nodes = ['s#unknown']
    all_nodes += sorted([f"s#{x}" for x in stats['node_stats']['node_categories']])
    all_nodes += ['o#unknown']
    all_nodes += sorted([f"o#{x}" for x in stats['node_stats']['node_categories']])
    all_nodes += sorted(stats['edge_stats']['provided_by'])

    fixed = set([x.split(' ')[0] if 'SciBite' in x else x for x in all_nodes])
    all_proper_nodes = sorted(list(fixed))
    sankey_nodes['label'] = all_proper_nodes

    for spo_key in stats['edge_stats']['count_by_spo']:
        triple = spo_key.split('-')
        source = all_proper_nodes.index(f"s#{triple[0]}")
        target = all_proper_nodes.index(f"o#{triple[2]}")
        sankey_links['source'].append(source)
        sankey_links['target'].append(target)
        sankey_links['value'].append(stats['edge_stats']['count_by_spo'][spo_key]['count'])
        sankey_links['label'].append(triple[1])

    for spo_key in stats['edge_stats']['count_by_spo']:
        triple = spo_key.split('-')
        source = all_proper_nodes.index(f"o#{triple[2]}")
        if 'provided_by' in stats['edge_stats']['count_by_spo'][spo_key]:
            for provided_by_key in stats['edge_stats']['count_by_spo'][spo_key]['provided_by']:
                if 'SciBite' in provided_by_key:
                    sanitized_key = provided_by_key.split(' ')[0]
                else:
                    sanitized_key = provided_by_key
                target = all_proper_nodes.index(sanitized_key)
                sankey_links['source'].append(source)
                sankey_links['target'].append(target)
                sankey_links['label'].append(str(stats['edge_stats']['count_by_spo'][spo_key]['provided_by'][provided_by_key]['count']))
                sankey_links['value'].append(stats['edge_stats']['count_by_spo'][spo_key]['provided_by'][provided_by_key]['count'])

    sankey_links['label'] = [x.split("#")[1] if '#' in x else x for x in sankey_links['label']]
    sankey_nodes['label'] = [x.split("#")[1] if '#' in x else x for x in sankey_nodes['label']]
    sankey['data'][0]['link'] = sankey_links
    return sankey

def generate_sankey_json_s2c2c2s(stats, **kwargs):
    """
    Sankey where col1 is source, col2 is category, col3 is category, and col4 is source
    """
    sankey = json.load(open('sankey_sample.json'))
    sankey_nodes = sankey['data'][0]['node']
    sankey_nodes['label'] = []
    sankey_nodes['color'] = sankey_nodes['color'] * 2
    sankey_nodes['x'] = []
    sankey_nodes['y'] = []
    sankey_links = sankey['data'][0]['link']
    sankey_links = {
        'source': [],
        'target': [],
        'label': [],
        'value': [],
        'color': sankey_links['color'] * 2,
    }

    sankey['layout']['title']['text'] = f"Sankey Plot for KG-COVID-19"
    all_nodes = sorted([f"l#{x}" for x in stats['edge_stats']['provided_by']])
    all_nodes += ['s#unknown']
    all_nodes += sorted([f"s#{x}" for x in stats['node_stats']['node_categories']])
    all_nodes += ['o#unknown']
    all_nodes += sorted([f"o#{x}" for x in stats['node_stats']['node_categories']])
    all_nodes += sorted([f"r#{x}" for x in stats['edge_stats']['provided_by']])
    fixed = set([x.split(' ')[0] if 'SciBite' in x else x for x in all_nodes])
    all_proper_nodes = sorted(list(fixed))
    sankey_nodes['label'] = all_proper_nodes

    for category_key in stats['node_stats']['count_by_category']:
        target = all_proper_nodes.index(f"s#{category_key}")
        if 'provided_by' in stats['node_stats']['count_by_category'][category_key]:
            for provided_by_key in stats['node_stats']['count_by_category'][category_key]['provided_by']:
                if 'SciBite' in provided_by_key:
                    sanitized_key = provided_by_key.split(' ')[0]
                else:
                    sanitized_key = provided_by_key
                source = all_proper_nodes.index(f"l#{sanitized_key}")
                sankey_links['source'].append(source)
                sankey_links['target'].append(target)
                sankey_links['value'].append(stats['node_stats']['count_by_category'][category_key]['provided_by'][provided_by_key]['count'])
                sankey_links['label'].append(str(stats['node_stats']['count_by_category'][category_key]['provided_by'][provided_by_key]['count']))

    for spo_key in stats['edge_stats']['count_by_spo']:
        triple = spo_key.split('-')
        source = all_proper_nodes.index(f"s#{triple[0]}")
        target = all_proper_nodes.index(f"o#{triple[2]}")
        sankey_links['source'].append(source)
        sankey_links['target'].append(target)
        sankey_links['value'].append(stats['edge_stats']['count_by_spo'][spo_key]['count'])
        sankey_links['label'].append(triple[1])

    for spo_key in stats['edge_stats']['count_by_spo']:
        triple = spo_key.split('-')
        source = all_proper_nodes.index(f"o#{triple[2]}")
        if 'provided_by' in stats['edge_stats']['count_by_spo'][spo_key]:
            for provided_by_key in stats['edge_stats']['count_by_spo'][spo_key]['provided_by']:
                if 'SciBite' in provided_by_key:
                    sanitized_key = provided_by_key.split(' ')[0]
                else:
                    sanitized_key = provided_by_key
                target = all_proper_nodes.index(f"r#{sanitized_key}")
                sankey_links['source'].append(source)
                sankey_links['target'].append(target)
                sankey_links['label'].append(str(stats['edge_stats']['count_by_spo'][spo_key]['provided_by'][provided_by_key]['count']))
                sankey_links['value'].append(stats['edge_stats']['count_by_spo'][spo_key]['provided_by'][provided_by_key]['count'])

    sankey_links['label'] = [x.split("#")[1] if '#' in x else x for x in sankey_links['label']]
    sankey_nodes['label'] = [x.split("#")[1] if '#' in x else x for x in sankey_nodes['label']]
    sankey['data'][0]['link'] = sankey_links
    return sankey


# ## Load stats from KG-COVID-19

# In[3]:


#stats = 'http://kg-hub.berkeleybop.io/merged_graph_stats.yaml'
#file = wget.download(stats)
stats = yaml.load(open('test_graph_stats.yaml'), Loader=yaml.FullLoader)


# ## Sankey plot with just source and category

# In[4]:


data = generate_sankey_json_s2c(stats)

opacity = 0.4
# change 'magenta' to its 'rgba' value to add opacity
data['data'][0]['node']['color'] = ['rgba(255,0,255, 0.8)' if color == "magenta" else color for color in data['data'][0]['node']['color']]
data['data'][0]['link']['color'] = [data['data'][0]['node']['color'][src].replace("0.8", str(opacity)) for src in data['data'][0]['link']['source']]

fig = go.Figure(data=[go.Sankey(
    # Define nodes
    node = dict(
      pad = 35,
      thickness = 15,
      line = dict(color = "black", width = 0.5),
      label =  data['data'][0]['node']['label'],
      color =  data['data'][0]['node']['color']
    ),
    # Add links
    link = dict(
      source =  data['data'][0]['link']['source'],
      target =  data['data'][0]['link']['target'],
      value =  data['data'][0]['link']['value'],
      label =  data['data'][0]['link']['label'],
      color =  data['data'][0]['link']['color']
))])

fig.update_layout(title_text="KG-COVID-19", font_size=9)
fig.show()


# ## Sankey plot with category-category associations, and source

# In[5]:


data = generate_sankey_json_c2c2s(stats)

opacity = 0.4
# change 'magenta' to its 'rgba' value to add opacity
data['data'][0]['node']['color'] = ['rgba(255,0,255, 0.8)' if color == "magenta" else color for color in data['data'][0]['node']['color']]
data['data'][0]['link']['color'] = [data['data'][0]['node']['color'][src].replace("0.8", str(opacity)) for src in data['data'][0]['link']['source']]

fig = go.Figure(data=[go.Sankey(
    # Define nodes
    node = dict(
      pad = 35,
      thickness = 15,
      line = dict(color = "black", width = 0.5),
      label =  data['data'][0]['node']['label'],
      color =  data['data'][0]['node']['color']
    ),
    # Add links
    link = dict(
      source =  data['data'][0]['link']['source'],
      target =  data['data'][0]['link']['target'],
      value =  data['data'][0]['link']['value'],
      label =  data['data'][0]['link']['label'],
      color =  data['data'][0]['link']['color']
))])

fig.update_layout(title_text="KG-COVID-19", font_size=9)
fig.show()


# ## Sankey plot with source, category-category associations, and source

# In[6]:


data = generate_sankey_json_s2c2c2s(stats)

opacity = 0.4
# change 'magenta' to its 'rgba' value to add opacity
data['data'][0]['node']['color'] = ['rgba(255,0,255, 0.8)' if color == "magenta" else color for color in data['data'][0]['node']['color']]
data['data'][0]['link']['color'] = [data['data'][0]['node']['color'][src].replace("0.8", str(opacity)) for src in data['data'][0]['link']['source']]

fig = go.Figure(data=[go.Sankey(
    # Define nodes
    node = dict(
      pad = 35,
      thickness = 15,
      line = dict(color = "black", width = 0.5),
      label =  data['data'][0]['node']['label'],
      color =  data['data'][0]['node']['color']
    ),
    # Add links
    link = dict(
      source =  data['data'][0]['link']['source'],
      target =  data['data'][0]['link']['target'],
      value =  data['data'][0]['link']['value'],
      label =  data['data'][0]['link']['label'],
      color =  data['data'][0]['link']['color']
))])

fig.update_layout(title_text="KG-COVID-19", font_size=9)
fig.show()


# In[7]:


# Note: If you would like to export these plots as high resolution PDF/PNG/SVG then the following 
# dependencies are required to be installed separately from your pip environment:
# Orca (https://github.com/plotly/orca)

fig.write_image('plot.pdf', format='pdf', width=1920, height=1080, scale=3.0)


# In[ ]:




