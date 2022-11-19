import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
  st.title("Make Profiles from a Stack Profile Data")
  st.header("ArcGISのスタック断面図のデータから断面図グラフを作成するサイト")
  st.text("ArcGISからcsv形式でエクスポートしたスタック断面図のデータをアップロードして、断面図の番号を指定してください。")
  uploaded_file = st.file_uploader("ファイルアップロード", type='csv')

  # uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
  if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
    # 断面の総数を調べる
    #num_lines = dataframe["LINE_ID"].max()
    line_min = dataframe["LINE_ID"].min()
    line_max = dataframe["LINE_ID"].max()
    num_lines = line_max - line_min + 1
    st.text(f"{str(num_lines)} lines are avairable.")
    if(num_lines):
      loi = st.selectbox('Select a target line', range(line_min, line_max + 1))
    
    if(loi):
      df_temp = dataframe[dataframe.LINE_ID == loi].loc[:, ['FIRST_DIST', 'FIRST_Z']]
      x_max, x_min = df_temp["FIRST_DIST"].max(), df_temp["FIRST_DIST"].min()
      y_max, y_min = df_temp["FIRST_Z"].max(), df_temp["FIRST_Z"].min()
      x_interval = st.selectbox('Select x tick interval', [1, 5, 10, 20, 25, 50 ,100],index = 1)
      y_interval = st.selectbox('Select y tick interval', [1, 5, 10, 20, 25, 50 ,100],index = 0)
      x1 = (int(x_min/x_interval) - 1) * x_interval
      x2 = (int(x_max/x_interval)+1) * x_interval
      y1 = (int(y_min/y_interval) - 1) * y_interval
      y2 = (int(y_max/y_interval)+1) * y_interval

      fig_scale = st.selectbox('Select fig scale', range(1, 4),index = 0)
      fig_scale_y = st.selectbox('Select y/x ratio', range(1, 11), index = 1)
      size_x, size_y = (x2 - x1)* fig_scale, (y2 - y1) * fig_scale * fig_scale_y
    
      fig = plt.figure(figsize=(size_x, size_y))
      plt.plot(df_temp["FIRST_DIST"], df_temp["FIRST_Z"], color="black")
      plt.xlim(x1, x2)
      plt.ylim(y1, y2)
      font_size = 60 * fig_scale
      plt.title('Line_' + str(loi),{'fontsize':font_size})     #文字サイズ
      plt.xlabel('Distance (m)',{'fontsize':font_size}) #文字サイズ
      plt.ylabel('Elevation (m)',{'fontsize':font_size}) #文字サイズ
      plt.tick_params(labelsize=font_size) #目盛りサイズ
      plt.xticks(np.arange(x1, x2 + 1, step = x_interval))
      plt.yticks(np.arange(y1, y2 + 1, step = y_interval))
      draw_hlines = st.checkbox('Horizontal Line',value=False)
      if(draw_hlines):
        gpoint = np.arange(y1, y2, y_interval)
        plt.hlines(gpoint,x1, x2, linewidth=0.3)
      st.pyplot(fig)

      @st.cache
      def convert_df(df):
          # IMPORTANT: Cache the conversion to prevent computation on every rerun
          return df.to_csv().encode('utf-8')

      csv = convert_df(df_temp)

      st.download_button(
          label="Download data as CSV",
          data=csv,
          file_name=f"{str(loi)}.csv",
          mime='text/csv',
      )

if __name__ == '__main__':
    main()
