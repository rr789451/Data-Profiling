# import streamlit as st
# import pandas as pd
# import numpy as np
# from ydata_profiling import ProfileReport
# from streamlit_pandas_profiling import st_profile_report
# from io import BytesIO
# from scipy.stats import zscore
# import seaborn as sns
# import matplotlib.pyplot as plt

# st.set_page_config(layout="wide")
# st.title("📊 Data Profiler")

# # Load file
# uploaded_file = st.file_uploader("Upload your utility data (CSV or Excel)", type=["csv", "xlsx"])

# def load_data(file):
#     if file.name.endswith(".csv"):
#         return pd.read_csv(file)
#     else:
#         return pd.read_excel(file)

# def detect_time_gaps(df, time_col='timestamp'):
#     df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
#     df = df.sort_values(time_col)
#     df["gap_hours"] = df[time_col].diff().dt.total_seconds().div(3600)
#     df["gap_flag"] = df["gap_hours"] > 6
#     return df

# def detect_zscore_anomalies(df, numeric_cols):
#     if not numeric_cols:
#         df["zscore_anomaly"] = False
#         return df
#     z_df = df[numeric_cols].apply(zscore)
#     anomalies = (np.abs(z_df) > 3)
#     df["zscore_anomaly"] = anomalies.any(axis=1)
#     return df

# def convert_df(df):
#     return df.to_csv(index=False).encode('utf-8')

# if uploaded_file:
#     df = load_data(uploaded_file)
#     original_df = df.copy()

#     st.subheader("📋 Raw Data Preview")
#     preview_df = df.head(10).copy()
#     preview_df.index = preview_df.index + 1
#     st.dataframe(preview_df, use_container_width=True)

#     time_col = st.selectbox("Select timestamp column (for gap detection)", options=df.columns)
#     numeric_default = df.select_dtypes(include=np.number).columns.tolist()
#     num_cols = st.multiselect("Select numeric columns (for anomaly detection)", options=numeric_default)

#     # Initialize flags
#     df["gap_flag"] = False
#     df["zscore_anomaly"] = False

#     # Detect gaps & anomalies
#     if time_col:
#         df = detect_time_gaps(df, time_col)
#     df = detect_zscore_anomalies(df, num_cols)

#     # Cleaning options
#     st.subheader("🧹 Data Cleaning Options")

#     if st.button("Drop duplicate rows"):
#         df = df.drop_duplicates()
#         st.success("✅ Duplicates dropped")

#     clean_option = st.radio("Fill missing values", ["None", "Fill with Mean", "Forward Fill"])
#     if clean_option == "Fill with Mean":
#         df = df.fillna(df.mean(numeric_only=True))
#         st.success("✅ Filled with means")
#     elif clean_option == "Forward Fill":
#         df = df.fillna(method='ffill')
#         st.success("✅ Forward-filled")

#     # Filter section
#     st.subheader("🔎 Filter Section")
#     filter_opt = st.radio("Choose data to view", ["All Rows", "Only Gap Rows", "Only Anomaly Rows", "Gap & Anomaly Rows"])

#     filter_df = df.copy()
#     if filter_opt == "Only Gap Rows":
#         filter_df = filter_df[filter_df["gap_flag"] == True]
#     elif filter_opt == "Only Anomaly Rows":
#         filter_df = filter_df[filter_df["zscore_anomaly"] == True]
#     elif filter_opt == "Gap & Anomaly Rows":
#         filter_df = filter_df[(filter_df["gap_flag"]) | (filter_df["zscore_anomaly"])]

#     # Shift index
#     filter_df_display = filter_df.copy()
#     filter_df_display.index = filter_df_display.index + 1
#     st.dataframe(filter_df_display, use_container_width=True)

#     # Chart section
#     st.subheader("📈 Chart Section")

#     st.markdown("#### 🟡 Missing Value Heatmap")
#     if df.isnull().values.any():
#         fig1, ax1 = plt.subplots()
#         sns.heatmap(df.isnull(), cbar=False, ax=ax1, cmap="YlOrBr")
#         st.pyplot(fig1)
#     else:
#         st.info("🟢 No missing values detected.")

#     if not num_cols:
#         num_cols = numeric_default

#     if num_cols:
#         st.markdown("#### 📊 Histogram of Selected Numeric Column")
#         if num_cols:
#             selected_hist_col = st.selectbox("Select column for histogram", num_cols, index=0)
#             fig2, ax2 = plt.subplots()
#             sns.histplot(df[selected_hist_col].dropna(), kde=True, ax=ax2)
#             ax2.set_title(f"Distribution of {selected_hist_col}")
#             st.pyplot(fig2)

#     st.markdown("#### 📉 Line Plot (Time Series)")
#     if time_col and num_cols:
#         selected_y = st.selectbox("Select Y-axis column for line plot", num_cols)
#         fig3, ax3 = plt.subplots()
#         df_sorted = df.sort_values(time_col)
#         ax3.plot(df_sorted[time_col], df_sorted[selected_y])
#         ax3.set_title(f"{selected_y} over Time")
#         ax3.set_xlabel(time_col)
#         ax3.set_ylabel(selected_y)
#         st.pyplot(fig3)

#     # Profiling Report
#     st.subheader("📑 Profiling Report")
#     profile = ProfileReport(df, title="Complete Utility Profile", explorative=True)
#     st_profile_report(profile)

#     # Export Section
#     st.subheader("📤 Export")
#     st.download_button("⬇️ Download Cleaned CSV", convert_df(df), "cleaned_data.csv", "text/csv")
#     st.download_button("⬇️ Download Full Report (HTML)", profile.to_html(), "profile_report.html", "text/html")

# else:
#     st.info("Upload a .csv or .xlsx file to begin.")


import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from io import BytesIO
from scipy.stats import zscore
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import psycopg2
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from shapely.geometry import Point, Polygon, LineString
import warnings
import json
from datetime import datetime, date
warnings.filterwarnings('ignore')

st.set_page_config(layout="wide")
st.title("📊 Enhanced Data Profiler with PostGIS Support")

# Initialize session state for data persistence
if 'current_table_data' not in st.session_state:
    st.session_state.current_table_data = None
if 'current_table_name' not in st.session_state:
    st.session_state.current_table_name = None
if 'current_table_is_spatial' not in st.session_state:
    st.session_state.current_table_is_spatial = False
if 'all_tables_data' not in st.session_state:
    st.session_state.all_tables_data = None

# Sidebar for data source selection
st.sidebar.title("🔌 Data Source")
data_source = st.sidebar.radio("Choose your data source:", ["📁 File Upload", "🗄️ PostGIS Database"])

# Database connection functions
@st.cache_resource
def connect_to_postgis(host, port, database, username, password):
    """Create connection to PostGIS database"""
    try:
        engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        st.error(f"❌ Connection failed: {e}")
        return None

def get_table_names(engine):
    """Get all table names from the database"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT tablename
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename
            """))
            
            rows = result.fetchall()
            if rows:
                table_names = [row[0] for row in rows]
                return pd.DataFrame({'tablename': table_names})
            else:
                return pd.DataFrame(columns=['tablename'])
                
    except Exception as e:
        st.warning(f"Primary query failed: {e}")
        try:
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT table_name
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_type = 'BASE TABLE'
                    ORDER BY table_name
                """))
                
                rows = result.fetchall()
                if rows:
                    table_names = [row[0] for row in rows]
                    return pd.DataFrame({'tablename': table_names})
                else:
                    return pd.DataFrame(columns=['tablename'])
                    
        except Exception as e2:
            st.error(f"Both queries failed: {e}, {e2}")
            return pd.DataFrame(columns=['tablename'])

def get_table_info(engine, table_name):
    """Get detailed information about a table"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default,
                    character_maximum_length
                FROM information_schema.columns 
                WHERE table_name = :table_name 
                AND table_schema = 'public'
                ORDER BY ordinal_position
            """), {"table_name": table_name})
            
            rows = result.fetchall()
            if rows:
                columns = ['column_name', 'data_type', 'is_nullable', 'column_default', 'character_maximum_length']
                data = [dict(zip(columns, row)) for row in rows]
                return pd.DataFrame(data)
            else:
                return pd.DataFrame(columns=['column_name', 'data_type', 'is_nullable', 'column_default', 'character_maximum_length'])
                
    except Exception as e:
        st.error(f"Error getting table info for {table_name}: {e}")
        return pd.DataFrame(columns=['column_name', 'data_type', 'is_nullable', 'column_default', 'character_maximum_length'])

def get_geometry_columns(engine, table_name):
    """Check if table has geometry columns"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    f_geometry_column as column_name,
                    type,
                    srid,
                    coord_dimension
                FROM geometry_columns 
                WHERE f_table_name = :table_name
            """), {"table_name": table_name})
            
            rows = result.fetchall()
            if rows:
                columns = ['column_name', 'type', 'srid', 'coord_dimension']
                data = [dict(zip(columns, row)) for row in rows]
                return pd.DataFrame(data)
            else:
                return pd.DataFrame(columns=['column_name', 'type', 'srid', 'coord_dimension'])
                
    except Exception as e:
        try:
            with engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT column_name
                    FROM information_schema.columns 
                    WHERE table_name = :table_name 
                    AND table_schema = 'public'
                    AND udt_name = 'geometry'
                """), {"table_name": table_name})
                
                rows = result.fetchall()
                if rows:
                    geom_columns = [row[0] for row in rows]
                    return pd.DataFrame({
                        'column_name': geom_columns,
                        'type': ['GEOMETRY'] * len(geom_columns),
                        'srid': [4326] * len(geom_columns),
                        'coord_dimension': [2] * len(geom_columns)
                    })
                else:
                    return pd.DataFrame(columns=['column_name', 'type', 'srid', 'coord_dimension'])
        except:
            return pd.DataFrame(columns=['column_name', 'type', 'srid', 'coord_dimension'])

def load_geospatial_data(engine, table_name, limit=None):
    """Load data from PostGIS table"""
    try:
        geom_cols = get_geometry_columns(engine, table_name)
        limit_clause = f"LIMIT {limit}" if limit else ""
        
        if not geom_cols.empty:
            geom_col = geom_cols.iloc[0]['column_name']
            query = f"SELECT * FROM {table_name} {limit_clause}"
            gdf = gpd.read_postgis(query, engine, geom_col=geom_col)
            return gdf, True
        else:
            query = f"SELECT * FROM {table_name} {limit_clause}"
            df = pd.read_sql(query, engine)
            return df, False
    except Exception as e:
        st.error(f"❌ Error loading data from {table_name}: {e}")
        return None, False

def get_table_statistics(engine, table_name):
    """Get basic statistics about the table"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) as row_count FROM {table_name}"))
            row_count = result.fetchone()[0]
            
            result = conn.execute(text(f"""
                SELECT pg_size_pretty(pg_total_relation_size('{table_name}')) as table_size
            """))
            table_size = result.fetchone()[0]
            
            return {'row_count': row_count, 'table_size': table_size}
    except Exception as e:
        st.warning(f"⚠️ Could not get statistics for {table_name}: {e}")
        return {'row_count': 'Unknown', 'table_size': 'Unknown'}

# File processing functions
def load_data(file):
    """Load data from uploaded file"""
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

def detect_time_gaps(df, time_col='timestamp'):
    """Detect time gaps in data"""
    df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
    df = df.sort_values(time_col)
    df["gap_hours"] = df[time_col].diff().dt.total_seconds().div(3600)
    df["gap_flag"] = df["gap_hours"] > 6
    return df

def detect_zscore_anomalies(df, numeric_cols):
    """Detect anomalies using z-score"""
    if not numeric_cols:
        df["zscore_anomaly"] = False
        return df
    z_df = df[numeric_cols].apply(zscore)
    anomalies = (np.abs(z_df) > 3)
    df["zscore_anomaly"] = anomalies.any(axis=1)
    return df

def convert_df(df):
    """Convert dataframe to CSV for download"""
    return df.to_csv(index=False).encode('utf-8')

def create_map(gdf, geom_col):
    """Create folium map from GeoDataFrame with proper zoom and bounds"""
    if gdf.empty:
        return None
    
    try:
        # Calculate bounds
        bounds = gdf.bounds
        min_lat, min_lon = bounds.miny.min(), bounds.minx.min()
        max_lat, max_lon = bounds.maxy.max(), bounds.maxx.max()
        
        # Calculate center
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2
        
        # Create map with initial center
        m = folium.Map(location=[center_lat, center_lon], zoom_start=2)
        
        # Add geometries to map
        for idx, row in gdf.iterrows():
            if row[geom_col] is not None and not pd.isna(row[geom_col]):
                try:
                    # Create popup content (exclude geometry column)
                    popup_items = []
                    for col, val in row.drop(geom_col).items():
                        if pd.notna(val):
                            popup_items.append(f"<b>{col}:</b> {val}")
                    popup_content = "<br>".join(popup_items)
                    
                    # Add to map based on geometry type
                    if row[geom_col].geom_type == 'Point':
                        folium.Marker(
                            location=[row[geom_col].y, row[geom_col].x],
                            popup=folium.Popup(popup_content, max_width=300),
                            tooltip=f"Row {idx + 1}"
                        ).add_to(m)
                    else:
                        folium.GeoJson(
                            row[geom_col].__geo_interface__,
                            popup=folium.Popup(popup_content, max_width=300),
                            tooltip=f"Row {idx + 1}"
                        ).add_to(m)
                except Exception as e:
                    continue  # Skip problematic geometries
        
        # Fit map to show all features with padding
        try:
            lat_margin = (max_lat - min_lat) * 0.1 if max_lat != min_lat else 0.1
            lon_margin = (max_lon - min_lon) * 0.1 if max_lon != min_lon else 0.1
            
            sw_corner = [min_lat - lat_margin, min_lon - lon_margin]
            ne_corner = [max_lat + lat_margin, max_lon + lon_margin]
            
            m.fit_bounds([sw_corner, ne_corner])
        except:
            # Fallback: set reasonable zoom based on coordinate range
            coord_range = max(max_lat - min_lat, max_lon - min_lon)
            if coord_range > 50:
                m.zoom_start = 3
            elif coord_range > 10:
                m.zoom_start = 5
            elif coord_range > 1:
                m.zoom_start = 8
            else:
                m.zoom_start = 12
        
        return m
    except Exception as e:
        st.error(f"Error creating map: {e}")
        return None

def safe_geojson_export(gdf):
    """Safely export GeoDataFrame to GeoJSON, handling problematic data types"""
    try:
        # Create a copy for export
        export_gdf = gdf.copy()
        
        # Handle problematic data types
        for col in export_gdf.columns:
            if col == export_gdf.geometry.name:
                continue  # Skip geometry column
            
            dtype = str(export_gdf[col].dtype)
            
            # Convert datetime and date columns
            if 'datetime' in dtype or dtype == 'object':
                for idx in export_gdf.index:
                    val = export_gdf.loc[idx, col]
                    if isinstance(val, (datetime, date)):
                        export_gdf.loc[idx, col] = str(val)
                    elif pd.isna(val):
                        export_gdf.loc[idx, col] = None
        
        # Convert to GeoJSON
        return export_gdf.to_json()
    
    except Exception as e:
        raise Exception(f"Cannot export to GeoJSON: {str(e)}. This table contains data types that are not JSON serializable (likely date/datetime columns).")

def render_analysis_section(df, is_geospatial, table_name):
    """Render the complete analysis section for loaded data"""
    
    st.markdown("---")
    st.subheader("📈 Data Analysis")
    
    # Geospatial visualization
    if is_geospatial and isinstance(df, gpd.GeoDataFrame):
        st.markdown("#### 🗺️ Geospatial Visualization")
        geom_col = df.geometry.name
        
        try:
            map_obj = create_map(df, geom_col)
            if map_obj:
                st_folium(map_obj, width=700, height=500)
            else:
                st.warning("⚠️ Could not create map - no valid geometries found")
        except Exception as e:
            st.error(f"❌ Error creating map: {e}")
        
        # Add spacing to prevent layout issues
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Spatial statistics
        st.markdown("#### 📊 Spatial Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            try:
                geom_types = df.geometry.geom_type.value_counts()
                st.write("**Geometry Types:**")
                for geom_type, count in geom_types.items():
                    st.write(f"• {geom_type}: {count}")
            except:
                st.write("Geometry type analysis unavailable")
        
        with col2:
            try:
                if hasattr(df.geometry, 'area') and df.geometry.geom_type.iloc[0] in ['Polygon', 'MultiPolygon']:
                    areas = df.geometry.area
                    st.metric("Avg Area", f"{areas.mean():.8f}")
                elif df.geometry.geom_type.iloc[0] in ['LineString', 'MultiLineString']:
                    lengths = df.geometry.length
                    st.metric("Avg Length", f"{lengths.mean():.8f}")
                else:
                    st.write("Area/Length not applicable")
            except:
                st.write("Area/Length calculation unavailable")
        
        with col3:
            try:
                bounds = df.total_bounds
                st.write("**Spatial Bounds:**")
                st.write(f"Min X: {bounds[0]:.6f}")
                st.write(f"Min Y: {bounds[1]:.6f}")
                st.write(f"Max X: {bounds[2]:.6f}")
                st.write(f"Max Y: {bounds[3]:.6f}")
            except:
                st.write("Bounds calculation unavailable")
    
    # Standard visualizations
    st.markdown("---")
    st.markdown("#### 🟡 Missing Value Analysis")
    if df.isnull().values.any():
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        sns.heatmap(df.isnull(), cbar=True, ax=ax1, cmap="YlOrRd")
        ax1.set_title("Missing Values Heatmap")
        st.pyplot(fig1)
        plt.close(fig1)
    else:
        st.info("🟢 No missing values detected.")
    
    # Numeric columns analysis
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    if numeric_cols:
        st.markdown("#### 📊 Distribution Analysis")
        selected_hist_col = st.selectbox(
            "Select column for histogram", 
            numeric_cols, 
            index=0, 
            key=f"hist_select_{table_name}"
        )
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.histplot(df[selected_hist_col].dropna(), kde=True, ax=ax2, bins=30)
        ax2.set_title(f"Distribution of {selected_hist_col}")
        st.pyplot(fig2)
        plt.close(fig2)
        
        # Correlation heatmap for numeric columns
        if len(numeric_cols) > 1:
            st.markdown("#### 🔥 Correlation Matrix")
            fig3, ax3 = plt.subplots(figsize=(10, 8))
            correlation_matrix = df[numeric_cols].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax3)
            ax3.set_title("Correlation Matrix")
            st.pyplot(fig3)
            plt.close(fig3)
    
    # Time series analysis
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    if datetime_cols and numeric_cols:
        st.markdown("#### 📉 Time Series Analysis")
        time_col = st.selectbox(
            "Select time column", 
            datetime_cols, 
            key=f"time_select_{table_name}"
        )
        y_col = st.selectbox(
            "Select Y-axis column", 
            numeric_cols, 
            key=f"y_select_{table_name}"
        )
        
        fig4, ax4 = plt.subplots(figsize=(12, 6))
        df_sorted = df.sort_values(time_col)
        ax4.plot(df_sorted[time_col], df_sorted[y_col], marker='o', markersize=2)
        ax4.set_title(f"{y_col} over Time")
        ax4.set_xlabel(time_col)
        ax4.set_ylabel(y_col)
        plt.xticks(rotation=45)
        st.pyplot(fig4)
        plt.close(fig4)
    
    # Profiling Report
    st.markdown("---")
    st.subheader("📑 Comprehensive Data Profiling Report")
    
    # Prepare data for profiling
    profile_df = df.copy()
    if is_geospatial and isinstance(df, gpd.GeoDataFrame):
        geom_col = df.geometry.name
        profile_df[geom_col] = profile_df[geom_col].astype(str)
    
    try:
        with st.spinner("Generating comprehensive profile report..."):
            profile = ProfileReport(
                profile_df, 
                title=f"Data Profile - {table_name}", 
                explorative=True,
                minimal=False
            )
            st_profile_report(profile)
    except Exception as e:
        st.error(f"❌ Error generating profile report: {e}")
        st.info("💡 Try with a smaller dataset or disable some profiling features")
    
    # Export Section
    st.markdown("---")
    st.subheader("📤 Export Options")
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = convert_df(df)
        st.download_button(
            "⬇️ Download as CSV", 
            csv_data, 
            f"{table_name}.csv", 
            "text/csv",
            key=f"csv_download_{table_name}"
        )
    
    with col2:
        if is_geospatial and isinstance(df, gpd.GeoDataFrame):
            try:
                geojson_data = safe_geojson_export(df)
                st.download_button(
                    "⬇️ Download as GeoJSON",
                    geojson_data,
                    f"{table_name}.geojson",
                    "application/json",
                    key=f"geojson_download_{table_name}"
                )
            except Exception as e:
                st.error(f"❌ GeoJSON export failed for {table_name}")
                st.info(f"💡 Reason: {str(e)}")
                st.info("🔄 Use CSV export instead, which handles all data types.")
        else:
            st.info("ℹ️ GeoJSON export only available for spatial data")

# Main application logic
if data_source == "📁 File Upload":
    # File upload functionality
    uploaded_file = st.file_uploader("Upload your utility data (CSV or Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        df = load_data(uploaded_file)
        original_df = df.copy()
        
        st.subheader("📋 Raw Data Preview")
        preview_df = df.head(10).copy()
        preview_df.index = range(1, len(preview_df) + 1)
        st.dataframe(preview_df, use_container_width=True)
        
        # Original file processing functionality
        time_col = st.selectbox("Select timestamp column (for gap detection)", options=df.columns)
        numeric_default = df.select_dtypes(include=np.number).columns.tolist()
        num_cols = st.multiselect("Select numeric columns (for anomaly detection)", options=numeric_default)

        # Initialize flags
        df["gap_flag"] = False
        df["zscore_anomaly"] = False

        # Detect gaps & anomalies
        if time_col:
            df = detect_time_gaps(df, time_col)
        df = detect_zscore_anomalies(df, num_cols)

        # Cleaning options
        st.subheader("🧹 Data Cleaning Options")

        if st.button("Drop duplicate rows"):
            df = df.drop_duplicates()
            st.success("✅ Duplicates dropped")

        clean_option = st.radio("Fill missing values", ["None", "Fill with Mean", "Forward Fill"])
        if clean_option == "Fill with Mean":
            df = df.fillna(df.mean(numeric_only=True))
            st.success("✅ Filled with means")
        elif clean_option == "Forward Fill":
            df = df.fillna(method='ffill')
            st.success("✅ Forward-filled")

        # Filter section
        st.subheader("🔎 Filter Section")
        filter_opt = st.radio("Choose data to view", ["All Rows", "Only Gap Rows", "Only Anomaly Rows", "Gap & Anomaly Rows"])

        filter_df = df.copy()
        if filter_opt == "Only Gap Rows":
            filter_df = filter_df[filter_df["gap_flag"] == True]
        elif filter_opt == "Only Anomaly Rows":
            filter_df = filter_df[filter_df["zscore_anomaly"] == True]
        elif filter_opt == "Gap & Anomaly Rows":
            filter_df = filter_df[(filter_df["gap_flag"]) | (filter_df["zscore_anomaly"])]

        # Display filtered data
        filter_df_display = filter_df.copy()
        filter_df_display.index = range(1, len(filter_df_display) + 1)
        st.dataframe(filter_df_display, use_container_width=True)
        
        # Render analysis for file data
        render_analysis_section(df, False, "Uploaded_File")

else:  # PostGIS Database
    st.sidebar.subheader("🔗 Database Connection")
    
    # Connection parameters
    col1, col2 = st.sidebar.columns(2)
    with col1:
        host = st.text_input("Host", value="localhost")
        database = st.text_input("Database", value="geodata")
    with col2:
        port = st.text_input("Port", value="5432")
        username = st.text_input("Username", value="postgres")
    
    password = st.sidebar.text_input("Password", type="password")
    
    # Quick connect for local Postgres.app
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Quick Connect (Postgres.app)**")
    if st.sidebar.button("🚀 Connect to Local Postgres.app"):
        import getpass
        local_username = getpass.getuser()
        engine = connect_to_postgis("localhost", "5432", "geodata", local_username, "")
        if engine:
            st.session_state.db_engine = engine
            st.sidebar.success(f"✅ Connected as {local_username}!")
        else:
            st.sidebar.error("❌ Failed to connect. Make sure Postgres.app is running and geodata database exists.")
    
    if st.sidebar.button("🔌 Connect to Database"):
        if all([host.strip(), port.strip(), database.strip(), username.strip()]):
            engine = connect_to_postgis(host.strip(), port.strip(), database.strip(), username.strip(), password)
            if engine:
                st.session_state.db_engine = engine
                st.sidebar.success("✅ Connected successfully!")
        else:
            missing_fields = []
            if not host.strip(): missing_fields.append("Host")
            if not port.strip(): missing_fields.append("Port") 
            if not database.strip(): missing_fields.append("Database")
            if not username.strip(): missing_fields.append("Username")
            st.sidebar.error(f"❌ Please fill in: {', '.join(missing_fields)}")
    
    # If connected, show table options
    if 'db_engine' in st.session_state:
        engine = st.session_state.db_engine
        
        try:
            # Get available tables
            tables_df = get_table_names(engine)
            
            if tables_df is not None and not tables_df.empty:
                table_names = tables_df['tablename'].tolist()
            else:
                table_names = []
            
            if table_names:
                st.sidebar.subheader("📋 Table Selection")
                
                # Option to select all tables or individual table
                selection_mode = st.sidebar.radio("Select:", ["📊 Individual Table", "📚 All Tables"])
                
                if selection_mode == "📊 Individual Table":
                    # Clear all tables data when switching to individual mode
                    if st.session_state.all_tables_data is not None:
                        st.session_state.all_tables_data = None
                    
                    selected_table = st.sidebar.selectbox("Choose a table:", table_names)
                    
                    # Clear data when table changes
                    if selected_table != st.session_state.current_table_name:
                        st.session_state.current_table_data = None
                        st.session_state.current_table_name = selected_table
                        st.session_state.current_table_is_spatial = False
                    
                    if selected_table:
                        # Show table information
                        st.subheader(f"📊 Table: {selected_table}")
                        
                        # Get table statistics
                        stats = get_table_statistics(engine, selected_table)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("📈 Total Rows", stats['row_count'])
                        with col2:
                            st.metric("💾 Table Size", stats['table_size'])
                        with col3:
                            # Check if it's geospatial
                            geom_cols = get_geometry_columns(engine, selected_table)
                            is_geo = "Yes" if not geom_cols.empty else "No"
                            st.metric("🗺️ Geospatial", is_geo)
                        
                        # Show table schema
                        with st.expander("🔍 Table Schema"):
                            table_info = get_table_info(engine, selected_table)
                            if not table_info.empty:
                                table_info_display = table_info.copy()
                                table_info_display.index = range(1, len(table_info_display) + 1)
                                st.dataframe(table_info_display, use_container_width=True)
                            else:
                                st.warning("No schema information available")
                        
                        # Load data with limit option
                        st.subheader("📋 Data Loading")
                        limit_data = st.checkbox("Limit rows for preview", value=True)
                        row_limit = st.slider("Number of rows to load", 10, 1000, 100) if limit_data else None
                        
                        if st.button(f"📥 Load Data from {selected_table}", key=f"load_{selected_table}"):
                            with st.spinner("Loading data..."):
                                data, is_geospatial = load_geospatial_data(engine, selected_table, row_limit)
                                
                                if data is not None:
                                    # Store in session state
                                    st.session_state.current_table_data = data
                                    st.session_state.current_table_is_spatial = is_geospatial
                                    st.success(f"✅ Loaded {len(data)} rows from {selected_table}")
                                    st.rerun()
                
                else:  # All Tables mode
                    # Clear individual table data when switching to all tables mode
                    if st.session_state.current_table_data is not None:
                        st.session_state.current_table_data = None
                        st.session_state.current_table_name = None
                    
                    st.subheader("📚 All Tables Overview")
                    
                    # Display tables with their info
                    table_overview = []
                    for table in table_names:
                        try:
                            stats = get_table_statistics(engine, table)
                            geom_cols = get_geometry_columns(engine, table)
                            is_geo = "Yes" if not geom_cols.empty else "No"
                            geom_type = geom_cols.iloc[0]['type'] if not geom_cols.empty else "N/A"
                            
                            table_overview.append({
                                'Table Name': table,
                                'Row Count': stats['row_count'],
                                'Size': stats['table_size'],
                                'Geospatial': is_geo,
                                'Geometry Type': geom_type
                            })
                        except Exception as e:
                            st.warning(f"Could not get info for table {table}: {e}")
                            table_overview.append({
                                'Table Name': table,
                                'Row Count': 'Error',
                                'Size': 'Error',
                                'Geospatial': 'Unknown',
                                'Geometry Type': 'Unknown'
                            })
                    
                    if table_overview:
                        overview_df = pd.DataFrame(table_overview)
                        overview_df.index = range(1, len(overview_df) + 1)
                        st.dataframe(overview_df, use_container_width=True)
                        
                        # Load all tables button
                        if st.button("📥 Load All Tables"):
                            all_tables_data = {}
                            progress_bar = st.progress(0)
                            
                            for i, table in enumerate(table_names):
                                with st.spinner(f"Loading {table}..."):
                                    data, is_geo = load_geospatial_data(engine, table, 100)
                                    if data is not None:
                                        all_tables_data[table] = {'data': data, 'is_geospatial': is_geo}
                                    progress_bar.progress((i + 1) / len(table_names))
                            
                            # Store in session state
                            st.session_state.all_tables_data = all_tables_data
                            st.success(f"✅ Loaded {len(all_tables_data)} tables")
                            st.rerun()
            
            else:
                st.warning("⚠️ No tables found in the database")
                
        except Exception as e:
            st.error(f"❌ Error accessing database: {e}")

    # INDIVIDUAL TABLE ANALYSIS - Display loaded individual table data (OUTSIDE all conditionals)
    if st.session_state.current_table_data is not None and st.session_state.current_table_name is not None:
        df = st.session_state.current_table_data
        is_geospatial = st.session_state.current_table_is_spatial
        table_name = st.session_state.current_table_name
        
        # Show data preview
        st.subheader(f"📋 Data from {table_name}")
        preview_df = df.head(10).copy()
        preview_df.index = range(1, len(preview_df) + 1)
        st.dataframe(preview_df, use_container_width=True)
        
        # Render complete analysis
        render_analysis_section(df, is_geospatial, table_name)

    # ALL TABLES ANALYSIS - Display loaded all tables data (OUTSIDE all conditionals)
    if st.session_state.all_tables_data is not None:
        all_tables_data = st.session_state.all_tables_data
        
        # Multi-table analysis
        st.subheader("📚 Multi-Table Analysis Results")
        
        summary_stats = []
        for table_name, table_info in all_tables_data.items():
            data = table_info['data']
            stats = {
                'Table': table_name,
                'Rows': len(data),
                'Columns': len(data.columns),
                'Numeric Columns': len(data.select_dtypes(include=np.number).columns),
                'Text Columns': len(data.select_dtypes(include='object').columns),
                'Missing Values': data.isnull().sum().sum(),
                'Geospatial': 'Yes' if table_info['is_geospatial'] else 'No'
            }
            summary_stats.append(stats)
        
        summary_df = pd.DataFrame(summary_stats)
        summary_df.index = range(1, len(summary_df) + 1)
        st.dataframe(summary_df, use_container_width=True)
        
        # Individual table selector for detailed analysis
        st.markdown("#### 🔍 Detailed Analysis of Individual Table")
        selected_for_analysis = st.selectbox(
            "Select table for detailed analysis:", 
            list(all_tables_data.keys()),
            key="all_tables_analysis_selector"
        )
        
        if selected_for_analysis:
            analysis_data = all_tables_data[selected_for_analysis]['data']
            is_geo = all_tables_data[selected_for_analysis]['is_geospatial']
            st.write(f"**Analyzing: {selected_for_analysis}**")
            
            # Show basic info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", len(analysis_data))
            with col2:
                st.metric("Columns", len(analysis_data.columns))
            with col3:
                st.metric("Missing Values", analysis_data.isnull().sum().sum())
            
            # Show data preview
            preview_display = analysis_data.head(10).copy()
            preview_display.index = range(1, len(preview_display) + 1)
            st.dataframe(preview_display, use_container_width=True)
            
            # Render full analysis for selected table
            render_analysis_section(analysis_data, is_geo, f"AllTables_{selected_for_analysis}")

# Footer with instructions
st.markdown("---")
st.markdown("""
### 📖 Instructions:
1. **File Upload Mode**: Upload CSV/Excel files for traditional data profiling
2. **PostGIS Mode**: Connect to your PostGIS database to analyze geospatial data
3. **Individual Table**: Analyze one table at a time with full geospatial features
4. **All Tables**: Get an overview of all tables in your database
5. **Export**: Download processed data as CSV or GeoJSON (for spatial data)

### 🛠️ Features:
- ✅ File and database connectivity
- ✅ Geospatial data visualization with interactive maps
- ✅ Comprehensive data profiling with ydata-profiling
- ✅ Anomaly detection and data cleaning
- ✅ Multi-format export options
- ✅ Spatial statistics and analysis

### 🗺️ Map Features:
- **Auto-zoom**: Maps automatically adjust to show all features
- **Smart bounds**: Proper padding around geometries
- **Multi-geometry support**: Points, lines, and polygons

### 📤 Export Notes:
- **CSV**: Works for all data types
- **GeoJSON**: Available for spatial data, may fail for tables with date columns
""")