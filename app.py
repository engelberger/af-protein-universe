
import ast, random, urllib.request
import matplotlib.pyplot as plt, seaborn as sns, pandas as pd, streamlit as st, st_aggrid, py3Dmol, stmol
st.set_page_config(layout="wide")

@st.cache_resource #https://docs.streamlit.io/library/advanced-features/caching
def read_pockets_():
    return pd.read_csv('https://gist.githubusercontent.com/jurgjn/9db4b11be6aca6553361c1e461fbeae6/raw/55d5206266cc79bbe24fac90569a4e7d17466888/pockets_score60_pLDDT90.tsv', sep='\t')

@st.cache_resource
def read_af2_v3_(af2_id):
    url_ = f'https://alphafold.ebi.ac.uk/files/AF-{af2_id}-F1-model_v3.pdb'
    with urllib.request.urlopen(url_) as url:
        return url.read().decode('utf-8')

st.write('# Enzyme activity predictions for dark clusters')
df_pockets_ = read_pockets_().drop(['xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax', 'cl_file', 'cl_isfile'], axis=1)
#st.dataframe(df_pockets_, height=200, use_container_width=True)

gb = st_aggrid.GridOptionsBuilder.from_dataframe(df_pockets_)
gb.configure_selection('single')
gb.configure_grid_options(domLayout='normal')
gridOptions = gb.build()

grid_response = st_aggrid.AgGrid(df_pockets_,
    gridOptions=gridOptions,
    height=200,
    width='100%',
    enable_enterprise_modules=False,
)
if len(grid_response['selected_rows']) > 0:
    af2_id_ = grid_response['selected_rows'][0]['struct_id']
    resid_ = grid_response['selected_rows'][0]['resid']
else:
    af2_id_ = df_pockets_.head(1).struct_id.squeeze()
    resid_ = df_pockets_.head(1).resid.squeeze()

pocket_resid_ = ast.literal_eval(resid_)

#selected_indices = st.selectbox('Select structure:', df_pockets_['struct_id'])
# https://github.com/deepmind/alphafold/issues/92#issuecomment-1005495687
# https://github.com/Intron7/alpha_viewer
# https://alphafold.ebi.ac.uk/files/AF-A0A1V6PM83-F1-model_v3.pdb

st.write(f'## {af2_id_}')
pdb_ = read_af2_v3_(af2_id_)
colors_pocket = {i: '#0072b2' for i in pocket_resid_}

xyzview = py3Dmol.view(data=pdb_, style={'stick':{}})
xyzview.setStyle({'cartoon': {
    #'color':'spectrum'
    'colorscheme': {
        'prop': 'resi',
        'map': colors_pocket,
}}})
xyzview.setBackgroundColor('#D3D3D3')
stmol.showmol(xyzview, height = 800, width=800)

fig, ax = plt.subplots()
sns.heatmap([[1,2,3], [2,3,2]], ax=ax)
st.write(fig)
