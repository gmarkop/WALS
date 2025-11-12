"""
WALS Local Explorer - A Flask web application for exploring WALS linguistic data
"""
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from data_loader import WALSDataLoader
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wals-local-explorer-key'

# Initialize data loader
data_loader = WALSDataLoader()

@app.route('/')
def index():
    """Home page with statistics and overview"""
    stats = data_loader.get_statistics()
    return render_template('index.html', stats=stats)

@app.route('/languages')
def languages():
    """Browse all languages"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    family = request.args.get('family', '')
    macroarea = request.args.get('macroarea', '')

    languages_data = data_loader.get_languages(
        page=page,
        per_page=50,
        search=search,
        family=family,
        macroarea=macroarea
    )

    families = data_loader.get_families()
    macroareas = data_loader.get_macroareas()

    return render_template(
        'languages.html',
        languages=languages_data['items'],
        page=page,
        total_pages=languages_data['total_pages'],
        families=families,
        macroareas=macroareas,
        search=search,
        selected_family=family,
        selected_macroarea=macroarea
    )

@app.route('/language/<language_id>')
def language_detail(language_id):
    """Detailed view of a specific language"""
    language = data_loader.get_language(language_id)
    if not language:
        return render_template('404.html', message=f"Language {language_id} not found"), 404

    values = data_loader.get_values_for_language(language_id)
    return render_template('language_detail.html', language=language, values=values)

@app.route('/features')
def features():
    """Browse all typological features"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    area = request.args.get('area', '')

    features_data = data_loader.get_features(
        page=page,
        per_page=30,
        search=search,
        area=area
    )

    areas = data_loader.get_areas()

    return render_template(
        'features.html',
        features=features_data['items'],
        page=page,
        total_pages=features_data['total_pages'],
        areas=areas,
        search=search,
        selected_area=area
    )

@app.route('/feature/<feature_id>')
def feature_detail(feature_id):
    """Detailed view of a specific feature"""
    feature = data_loader.get_feature(feature_id)
    if not feature:
        return render_template('404.html', message=f"Feature {feature_id} not found"), 404

    codes = data_loader.get_codes_for_feature(feature_id)
    values = data_loader.get_values_for_feature(feature_id)

    return render_template(
        'feature_detail.html',
        feature=feature,
        codes=codes,
        values=values
    )

@app.route('/search')
def search():
    """Global search across languages and features"""
    query = request.args.get('q', '')
    category = request.args.get('category', 'all')

    results = {
        'languages': [],
        'features': [],
        'query': query
    }

    if query:
        if category in ['all', 'languages']:
            results['languages'] = data_loader.search_languages(query)
        if category in ['all', 'features']:
            results['features'] = data_loader.search_features(query)

    return render_template('search.html', results=results, category=category)

@app.route('/map')
def map_view():
    """Interactive map view of languages"""
    return render_template('map.html')

@app.route('/api/languages/geo')
def api_languages_geo():
    """API endpoint for language geographic data"""
    languages = data_loader.get_all_languages_geo()
    return jsonify(languages)

@app.route('/api/feature/<feature_id>/distribution')
def api_feature_distribution(feature_id):
    """API endpoint for feature value distribution"""
    distribution = data_loader.get_feature_distribution(feature_id)
    return jsonify(distribution)

@app.route('/statistics')
def statistics():
    """Statistics and data visualizations"""
    stats = data_loader.get_detailed_statistics()
    return render_template('statistics.html', stats=stats)

@app.route('/about')
def about():
    """About WALS and this application"""
    return render_template('about.html')

@app.route('/export/<format>')
def export_data(format):
    """Export data in various formats"""
    if format not in ['json', 'csv']:
        return "Invalid format", 400

    # This is a placeholder - implement actual export functionality as needed
    return jsonify({"message": "Export functionality coming soon"})

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', message="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html', message="Internal server error"), 500

if __name__ == '__main__':
    print("=" * 60)
    print("WALS Local Explorer")
    print("=" * 60)
    print("Starting server...")
    print("Open your browser and navigate to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
