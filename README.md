# 📊 Enhanced Data Profiler with PostGIS Support

A comprehensive data profiling and analysis tool built with Streamlit that supports both traditional file uploads and geospatial PostGIS databases. Perfect for analyzing utility data, geospatial datasets, and performing comprehensive data quality assessments.

## 🌟 Features

### 📁 File Upload Mode
- **Multi-format Support**: CSV and Excel files
- **Data Cleaning**: Duplicate removal, missing value handling, forward fill
- **Anomaly Detection**: Z-score based outlier detection
- **Time Gap Analysis**: Detect temporal gaps in time series data
- **Interactive Filtering**: Filter by anomalies, gaps, or combinations

### 🗄️ PostGIS Database Mode
- **Direct Database Connection**: Connect to any PostGIS-enabled PostgreSQL database
- **Geospatial Visualization**: Interactive maps with Folium for points, lines, and polygons
- **Spatial Statistics**: Geometry analysis, bounds calculation, area/length metrics
- **Multi-table Analysis**: Analyze individual tables or compare across all tables
- **Smart Export**: CSV for all data types, GeoJSON for spatial data with error handling

### 📈 Analysis Features
- **Comprehensive Profiling**: Powered by ydata-profiling
- **Interactive Visualizations**: Missing value heatmaps, correlation matrices, histograms
- **Time Series Analysis**: Temporal trend visualization
- **Spatial Analytics**: Geometry type analysis, spatial bounds, area calculations
- **Export Options**: Download as CSV, GeoJSON, or HTML reports

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL with PostGIS (for database features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd enhanced-data-profiler
   ```

2. **Install Python dependencies**
   ```bash
   pip install streamlit pandas numpy geopandas ydata-profiling streamlit-pandas-profiling scipy seaborn matplotlib psycopg2-binary sqlalchemy folium streamlit-folium plotly shapely
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🗄️ PostGIS Database Setup

### 🍎 macOS Installation

#### Option 1: Postgres.app (Recommended)

1. **Download and Install**
   - Visit [https://postgresapp.com/](https://postgresapp.com/)
   - Download the latest version
   - Drag to Applications folder and launch

2. **Configure PATH**
   ```bash
   echo 'export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Verify Installation**
   ```bash
   which psql
   # Should output: /Applications/Postgres.app/Contents/Versions/latest/bin/psql
   ```

#### Option 2: Homebrew

```bash
# Install PostgreSQL and PostGIS
brew install postgresql postgis

# Start PostgreSQL service
brew services start postgresql

# Create a database user
createuser -s $(whoami)
```

### 🪟 Windows Installation

#### Option 1: PostgreSQL Installer (Recommended)

1. **Download PostgreSQL**
   - Go to [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
   - Download the latest PostgreSQL installer
   - Run the installer as Administrator

2. **Installation Steps**
   - Choose installation directory (default: `C:\Program Files\PostgreSQL\15\`)
   - Set password for postgres user (remember this!)
   - Set port (default: 5432)
   - Select locale (default is fine)
   - **Important**: In the component selection, ensure "pgAdmin 4" and "Command Line Tools" are selected

3. **Install PostGIS**
   - After PostgreSQL installation, run "Application Stack Builder"
   - Select your PostgreSQL installation
   - Under "Spatial Extensions", select "PostGIS"
   - Complete the installation

4. **Add to System PATH**
   - Open System Properties → Advanced → Environment Variables
   - Add to PATH: `C:\Program Files\PostgreSQL\15\bin`
   - Restart Command Prompt/PowerShell

5. **Verify Installation**
   ```cmd
   psql --version
   # Should show PostgreSQL version
   ```

#### Option 2: Using Chocolatey

```powershell
# Install Chocolatey (if not already installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install PostgreSQL
choco install postgresql

# Install PostGIS (may require manual setup)
choco install postgis
```

### 🐧 Linux Installation (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install PostgreSQL and PostGIS
sudo apt install postgresql postgresql-contrib postgis postgresql-15-postgis-3

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create user and database
sudo -u postgres createuser --superuser $USER
sudo -u postgres createdb $USER
```

## 🛠️ Database Setup

### Create Sample Database

#### For macOS/Linux:
```bash
# Create the geodata database
createdb geodata

# Enable PostGIS extensions
psql -d geodata -c "CREATE EXTENSION IF NOT EXISTS postgis;"
psql -d geodata -c "CREATE EXTENSION IF NOT EXISTS postgis_topology;"
psql -d geodata -c "CREATE EXTENSION IF NOT EXISTS postgis_raster;"

# Verify PostGIS installation
psql -d geodata -c "SELECT PostGIS_Version();"
```

#### For Windows:
```cmd
# Open Command Prompt as Administrator
# Create the geodata database
createdb -U postgres geodata

# Enable PostGIS extensions (enter postgres password when prompted)
psql -U postgres -d geodata -c "CREATE EXTENSION IF NOT EXISTS postgis;"
psql -U postgres -d geodata -c "CREATE EXTENSION IF NOT EXISTS postgis_topology;"
psql -U postgres -d geodata -c "CREATE EXTENSION IF NOT EXISTS postgis_raster;"

# Verify PostGIS installation
psql -U postgres -d geodata -c "SELECT PostGIS_Version();"
```

### Load Sample Data

The repository includes `setup_sample_data.sql` with geospatial data for testing:

#### For macOS/Linux:
```bash
# Execute the sample data script
psql -d geodata -f setup_sample_data.sql
```

#### For Windows:
```cmd
# Execute the sample data script
psql -U postgres -d geodata -f setup_sample_data.sql
```

### Sample Data Tables

The script creates 6 tables with different geometry types:

| Table | Geometry Type | Description | Records |
|-------|---------------|-------------|---------|
| `cities` | Point | Major world cities with population data | 12 |
| `countries` | Polygon | Country boundaries with GDP data | 5 |
| `roads` | LineString | Road networks with speed limits | 6 |
| `utility_infrastructure` | Mixed | Power plants, pipelines, service areas | 10 |
| `weather_stations` | Point | Weather monitoring stations with sensor data | 6 |
| `admin_boundaries` | Polygon | Administrative boundaries | 5 |

### Verify Sample Data

#### For macOS/Linux:
```bash
# Check tables were created
psql -d geodata -c "\dt"

# Verify geometry columns
psql -d geodata -c "SELECT f_table_name, f_geometry_column, type FROM geometry_columns;"

# Count records in each table
psql -d geodata -c "
SELECT 'cities' as table_name, COUNT(*) FROM cities
UNION ALL SELECT 'countries', COUNT(*) FROM countries  
UNION ALL SELECT 'roads', COUNT(*) FROM roads
UNION ALL SELECT 'utility_infrastructure', COUNT(*) FROM utility_infrastructure
UNION ALL SELECT 'weather_stations', COUNT(*) FROM weather_stations
UNION ALL SELECT 'admin_boundaries', COUNT(*) FROM admin_boundaries;"
```

#### For Windows:
```cmd
# Check tables were created
psql -U postgres -d geodata -c "\dt"

# Verify geometry columns
psql -U postgres -d geodata -c "SELECT f_table_name, f_geometry_column, type FROM geometry_columns;"

# Count records in each table
psql -U postgres -d geodata -c "SELECT 'cities' as table_name, COUNT(*) FROM cities UNION ALL SELECT 'countries', COUNT(*) FROM countries UNION ALL SELECT 'roads', COUNT(*) FROM roads UNION ALL SELECT 'utility_infrastructure', COUNT(*) FROM utility_infrastructure UNION ALL SELECT 'weather_stations', COUNT(*) FROM weather_stations UNION ALL SELECT 'admin_boundaries', COUNT(*) FROM admin_boundaries;"
```

## 📖 Usage Guide

### File Upload Mode

1. Select "📁 File Upload" in the sidebar
2. Upload a CSV or Excel file
3. Configure timestamp and numeric columns for analysis
4. Use data cleaning options as needed
5. Apply filters to focus on specific data subsets
6. View comprehensive analysis and download results

### PostGIS Database Mode

1. Select "🗄️ PostGIS Database" in the sidebar
2. **Quick Connect** (macOS only): Click "🚀 Connect to Local Postgres.app"
3. **Manual Connect**: Enter connection details and click "🔌 Connect to Database"
4. Choose analysis mode:
   - **Individual Table**: Analyze one table with full features
   - **All Tables**: Overview and comparison across all tables

#### Connection Settings

**For macOS (Postgres.app):**
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `geodata`
- **Username**: Your macOS username (run `whoami` to check)
- **Password**: Leave blank

**For Windows:**
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `geodata`
- **Username**: `postgres`
- **Password**: The password you set during installation

**For Linux:**
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `geodata`
- **Username**: Your Linux username
- **Password**: Leave blank (or your user password)

### Individual Table Analysis

1. Select table from dropdown
2. Configure row limits if needed (recommended: 100 rows for initial exploration)
3. Click "📥 Load Data from [table]"
4. Explore features:
   - **Interactive Maps**: Click on features to see details
   - **Spatial Statistics**: Geometry analysis and bounds
   - **Data Quality**: Missing values, correlations
   - **Profiling Reports**: Comprehensive data overview
   - **Export Options**: CSV and GeoJSON downloads

### All Tables Analysis

1. Click "📥 Load All Tables" (loads 100 rows per table)
2. View multi-table comparison summary
3. Select individual tables for detailed analysis
4. Compare metrics across all tables
5. Export individual table data

## 🗺️ Geospatial Features

### Map Visualization
- **Auto-zoom**: Maps automatically fit to show all features
- **Multi-geometry Support**: Points, lines, polygons, and mixed types
- **Interactive Popups**: Click features to see attribute data
- **Smart Bounds**: Proper padding around geometries for optimal viewing

### Spatial Statistics
- **Geometry Types**: Count and distribution analysis
- **Area Calculations**: For polygon geometries (countries, admin boundaries)
- **Length Calculations**: For line geometries (roads, pipelines)
- **Spatial Bounds**: Coordinate extents and bounding boxes
- **SRID Information**: Coordinate reference system details

### Export Capabilities
- **CSV Export**: Universal format for all data types
- **GeoJSON Export**: Standards-compliant spatial format
- **Automatic Error Handling**: Clear messages when exports fail
- **Date Column Handling**: Converts problematic data types automatically

## 🔧 Troubleshooting

### Connection Issues

#### "Connection failed" Error
**macOS:**
- Ensure Postgres.app is running (elephant icon in menu bar)
- Check database name exists: `psql -l`
- Verify username with: `whoami`

**Windows:**
- Ensure PostgreSQL service is running:
  - Open Services (services.msc)
  - Look for "postgresql-x64-15" service
  - Start if not running
- Use username: `postgres`
- Use the password you set during installation

**Linux:**
- Check PostgreSQL status: `sudo systemctl status postgresql`
- Start if needed: `sudo systemctl start postgresql`

#### "Database does not exist" Error
```bash
# Create the database if it doesn't exist
createdb geodata  # macOS/Linux
createdb -U postgres geodata  # Windows
```

### Installation Issues

#### psycopg2-binary Installation Fails

**macOS:**
```bash
# Ensure PostgreSQL is in PATH
export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"
pip install psycopg2-binary
```

**Windows:**
```cmd
# Install Microsoft C++ Build Tools if needed
# Then try:
pip install psycopg2-binary
# Alternative:
conda install psycopg2
```

**Linux:**
```bash
# Install build dependencies
sudo apt-get install python3-dev libpq-dev
pip install psycopg2-binary
```

#### Geopandas Installation Issues
```bash
# Use conda for better dependency management
conda install -c conda-forge geopandas
# Or use conda-forge for all geospatial packages
conda install -c conda-forge geopandas folium streamlit plotly
```

### Data Issues

#### GeoJSON Export Fails
- **Common Cause**: Tables with date/datetime columns
- **Solution**: Use CSV export instead
- **Tables Affected**: `admin_boundaries`, `weather_stations`, `utility_infrastructure`
- **Tables That Work**: `cities`, `countries`, `roads`

#### Map Not Displaying
- Verify geometries are valid (not NULL)
- Check coordinate reference system (should be EPSG:4326)
- Ensure table has geometry column in `geometry_columns` view

#### No Tables Found
- Verify PostGIS extensions are installed
- Check you're connected to the correct database
- Ensure sample data was loaded successfully

### Performance Issues

#### Large Dataset Loading
- Use row limits (slider in app)
- Start with 100 rows for exploration
- Increase gradually based on system performance

## 📦 Dependencies

### Core Requirements
```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.21.0
geopandas>=0.12.0
ydata-profiling>=4.0.0
streamlit-pandas-profiling>=0.1.3
```

### Database & Geospatial
```
psycopg2-binary>=2.9.0
sqlalchemy>=1.4.0
shapely>=2.0.0
folium>=0.14.0
streamlit-folium>=0.13.0
```

### Visualization & Analysis
```
matplotlib>=3.5.0
seaborn>=0.11.0
plotly>=5.10.0
scipy>=1.9.0
```

### Complete Installation Command
```bash
pip install streamlit pandas numpy geopandas ydata-profiling streamlit-pandas-profiling scipy seaborn matplotlib psycopg2-binary sqlalchemy folium streamlit-folium plotly shapely
```

## 📁 Project Structure

```
enhanced-data-profiler/
├── app.py                      # Main Streamlit application
├── setup_sample_data.sql       # Sample PostGIS data (6 tables)
├── README.md                   # This documentation
├── large_utility_data.csv      # Sample CSV data
├── .gitignore                  # Git ignore patterns
```

## 🔒 Security Considerations

### Database Connections
- **Local Development**: Use local PostgreSQL instances
- **Production**: Implement proper authentication and SSL
- **Credentials**: Never commit passwords to version control
- **Network**: Restrict database access to necessary IPs only

### Data Privacy
- **Sensitive Data**: Be cautious with personal or confidential information
- **Export Controls**: Review data before downloading
- **Access Logs**: Monitor database access and usage patterns

## 🚀 Performance Optimization

### Database Performance
- **Indexing**: Create spatial indexes on geometry columns
- **Query Limits**: Use row limits for large datasets
- **Connection Pooling**: For high-traffic deployments

### Application Performance
- **Memory Management**: Monitor RAM usage with large datasets
- **Caching**: Leverage Streamlit's caching decorators
- **Concurrent Users**: Consider resource limits for multi-user scenarios

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Make your changes
5. Test thoroughly on your platform
6. Submit a pull request

### Code Standards
- **Python**: Follow PEP 8 style guidelines
- **Documentation**: Update README for any new features
- **Testing**: Test on multiple operating systems
- **Dependencies**: Minimize new dependencies

## 📞 Support

### Getting Help
- **Documentation**: Check this README first

### Known Limitations
- **Large Datasets**: Performance may degrade with >10,000 records
- **Complex Geometries**: Very detailed polygons may affect map rendering
- **Browser Memory**: Large profiling reports may consume significant RAM
- **Export Size**: GeoJSON exports limited by browser download capabilities

## 🙏 Acknowledgments

- **[Streamlit](https://streamlit.io/)** - Amazing web framework for data apps
- **[PostGIS](https://postgis.net/)** - Powerful spatial database capabilities
- **[ydata-profiling](https://github.com/ydataai/ydata-profiling)** - Comprehensive data profiling
- **[Folium](https://python-visualization.github.io/folium/)** - Beautiful interactive maps
- **[GeoPandas](https://geopandas.org/)** - Geospatial data analysis in Python

---

**🌟 Star this repository if you find it useful!**

**📧 Questions? Open an issue or start a discussion.**

**🚀 Ready to explore your data? Run `streamlit run app.py` and get started!**