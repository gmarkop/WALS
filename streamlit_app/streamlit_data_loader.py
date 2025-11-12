"""
Data loader for WALS Streamlit app
Handles loading and caching of CLDF data with Streamlit optimizations
"""

import streamlit as st
from pathlib import Path
import csv
import math

class WALSStreamlitLoader:
    def __init__(self, cldf_path=None):
        """Initialize the data loader with CLDF dataset path"""
        if cldf_path is None:
            # Try to find cldf directory relative to app
            base_path = Path(__file__).parent.parent
            cldf_path = base_path / 'cldf'

        self.cldf_path = Path(cldf_path)
        self.data_available = self.cldf_path.exists()

        # Data will be loaded lazily
        self._languages = None
        self._features = None
        self._codes = None
        self._values = None

    @st.cache_data
    def _load_csv(_self, filename):
        """Load a CSV file from CLDF directory (cached)"""
        filepath = _self.cldf_path / filename
        if not filepath.exists():
            return []

        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def _ensure_data_loaded(self):
        """Ensure all data is loaded (lazy loading)"""
        if self._languages is None:
            if self.data_available:
                self._load_cldf_data()
            else:
                self._load_sample_data()

    def _load_cldf_data(self):
        """Load data from CLDF files"""
        try:
            self._languages = self._load_csv('languages.csv')
            self._features = self._load_csv('parameters.csv')
            self._codes = self._load_csv('codes.csv')
            self._values = self._load_csv('values.csv')
        except Exception as e:
            st.error(f"Error loading CLDF data: {e}")
            self._load_sample_data()

    def _load_sample_data(self):
        """Load sample data for demonstration"""
        self._languages = [
            {
                'ID': 'eng', 'Name': 'English', 'Latitude': '51.5', 'Longitude': '-0.1',
                'Macroarea': 'Eurasia', 'Family': 'Indo-European', 'Genus': 'Germanic',
                'ISO639P3code': 'eng', 'Glottocode': 'stan1293'
            },
            {
                'ID': 'spa', 'Name': 'Spanish', 'Latitude': '40.4', 'Longitude': '-3.7',
                'Macroarea': 'Eurasia', 'Family': 'Indo-European', 'Genus': 'Romance',
                'ISO639P3code': 'spa', 'Glottocode': 'stan1288'
            },
            {
                'ID': 'cmn', 'Name': 'Mandarin Chinese', 'Latitude': '39.9', 'Longitude': '116.4',
                'Macroarea': 'Eurasia', 'Family': 'Sino-Tibetan', 'Genus': 'Chinese',
                'ISO639P3code': 'cmn', 'Glottocode': 'mand1415'
            },
            {
                'ID': 'ara', 'Name': 'Arabic', 'Latitude': '30.0', 'Longitude': '31.2',
                'Macroarea': 'Eurasia', 'Family': 'Afro-Asiatic', 'Genus': 'Semitic',
                'ISO639P3code': 'ara', 'Glottocode': 'stan1318'
            },
            {
                'ID': 'jpn', 'Name': 'Japanese', 'Latitude': '35.7', 'Longitude': '139.7',
                'Macroarea': 'Eurasia', 'Family': 'Japanese', 'Genus': 'Japanese',
                'ISO639P3code': 'jpn', 'Glottocode': 'nucl1643'
            },
        ]

        self._features = [
            {'ID': '81A', 'Name': 'Order of Subject, Object and Verb', 'Chapter_ID': 's4'},
            {'ID': '1A', 'Name': 'Consonant Inventories', 'Chapter_ID': 's1'},
            {'ID': '2A', 'Name': 'Vowel Quality Inventories', 'Chapter_ID': 's1'},
        ]

        self._codes = [
            {'ID': '81A-1', 'Parameter_ID': '81A', 'Name': 'SOV', 'Number': '1'},
            {'ID': '81A-2', 'Parameter_ID': '81A', 'Name': 'SVO', 'Number': '2'},
            {'ID': '81A-3', 'Parameter_ID': '81A', 'Name': 'VSO', 'Number': '3'},
            {'ID': '1A-1', 'Parameter_ID': '1A', 'Name': 'Small', 'Number': '1'},
            {'ID': '1A-2', 'Parameter_ID': '1A', 'Name': 'Moderately small', 'Number': '2'},
            {'ID': '1A-3', 'Parameter_ID': '1A', 'Name': 'Average', 'Number': '3'},
        ]

        self._values = [
            {'ID': 'eng-81A', 'Language_ID': 'eng', 'Parameter_ID': '81A', 'Code_ID': '81A-2', 'Value': '2'},
            {'ID': 'spa-81A', 'Language_ID': 'spa', 'Parameter_ID': '81A', 'Code_ID': '81A-2', 'Value': '2'},
            {'ID': 'jpn-81A', 'Language_ID': 'jpn', 'Parameter_ID': '81A', 'Code_ID': '81A-1', 'Value': '1'},
            {'ID': 'ara-81A', 'Language_ID': 'ara', 'Parameter_ID': '81A', 'Code_ID': '81A-3', 'Value': '3'},
        ]

    def get_statistics(self):
        """Get basic statistics about the dataset"""
        self._ensure_data_loaded()
        return {
            'languages': len(self._languages),
            'features': len(self._features),
            'values': len(self._values),
            'families': len(self.get_families()),
            'data_available': self.data_available
        }

    def get_all_languages(self):
        """Get all languages"""
        self._ensure_data_loaded()
        return self._languages

    def get_language(self, language_id):
        """Get a specific language by ID"""
        self._ensure_data_loaded()
        for lang in self._languages:
            if lang.get('ID') == language_id:
                return lang
        return None

    def get_families(self):
        """Get list of all language families"""
        self._ensure_data_loaded()
        families = set()
        for lang in self._languages:
            family = lang.get('Family', '')
            if family:
                families.add(family)
        return sorted(families)

    def get_macroareas(self):
        """Get list of all macroareas"""
        self._ensure_data_loaded()
        areas = set()
        for lang in self._languages:
            area = lang.get('Macroarea', '')
            if area:
                areas.add(area)
        return sorted(areas)

    def get_all_features(self):
        """Get all features"""
        self._ensure_data_loaded()
        return self._features

    def get_feature(self, feature_id):
        """Get a specific feature by ID"""
        self._ensure_data_loaded()
        for feature in self._features:
            if feature.get('ID') == feature_id:
                return feature
        return None

    def get_codes_for_feature(self, feature_id):
        """Get all possible codes/values for a feature"""
        self._ensure_data_loaded()
        return [c for c in self._codes if c.get('Parameter_ID') == feature_id]

    def get_values_for_language(self, language_id):
        """Get all feature values for a specific language"""
        self._ensure_data_loaded()
        values = [v for v in self._values if v.get('Language_ID') == language_id]

        # Enrich with feature and code information
        enriched = []
        for value in values:
            feature = self.get_feature(value.get('Parameter_ID'))
            code = next((c for c in self._codes if c.get('ID') == value.get('Code_ID')), None)

            enriched.append({
                **value,
                'Feature_Name': feature.get('Name', '') if feature else '',
                'Code_Name': code.get('Name', '') if code else ''
            })

        return enriched

    def get_values_for_feature(self, feature_id):
        """Get all language values for a specific feature"""
        self._ensure_data_loaded()
        values = [v for v in self._values if v.get('Parameter_ID') == feature_id]

        # Enrich with language information
        enriched = []
        for value in values:
            language = self.get_language(value.get('Language_ID'))
            code = next((c for c in self._codes if c.get('ID') == value.get('Code_ID')), None)

            enriched.append({
                **value,
                'Language_Name': language.get('Name', '') if language else '',
                'Code_Name': code.get('Name', '') if code else ''
            })

        return enriched

    def search_languages(self, query):
        """Search languages by name or ID"""
        self._ensure_data_loaded()
        if not query:
            return []

        query_lower = query.lower()
        results = []
        for lang in self._languages:
            if (query_lower in lang.get('Name', '').lower() or
                query_lower in lang.get('ID', '').lower() or
                query_lower in lang.get('Family', '').lower()):
                results.append(lang)
        return results[:100]  # Limit to 100 results

    def search_features(self, query):
        """Search features by name or ID"""
        self._ensure_data_loaded()
        if not query:
            return []

        query_lower = query.lower()
        results = []
        for feature in self._features:
            if (query_lower in feature.get('Name', '').lower() or
                query_lower in feature.get('ID', '').lower()):
                results.append(feature)
        return results[:100]

    def get_detailed_statistics(self):
        """Get detailed statistics for visualization"""
        self._ensure_data_loaded()
        stats = self.get_statistics()

        # Count by family
        family_counts = {}
        for lang in self._languages:
            family = lang.get('Family', 'Unknown')
            family_counts[family] = family_counts.get(family, 0) + 1

        # Count by macroarea
        macroarea_counts = {}
        for lang in self._languages:
            area = lang.get('Macroarea', 'Unknown')
            macroarea_counts[area] = macroarea_counts.get(area, 0) + 1

        stats['family_distribution'] = family_counts
        stats['macroarea_distribution'] = macroarea_counts

        # Create sorted list for table display
        sorted_families = sorted(family_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        stats['top_families'] = sorted_families

        return stats

    def get_languages_with_coordinates(self):
        """Get all languages with valid geographic coordinates"""
        self._ensure_data_loaded()
        languages_with_coords = []

        for lang in self._languages:
            lat = lang.get('Latitude')
            lon = lang.get('Longitude')

            if lat and lon:
                try:
                    languages_with_coords.append({
                        'id': lang.get('ID'),
                        'name': lang.get('Name'),
                        'lat': float(lat),
                        'lon': float(lon),
                        'family': lang.get('Family', 'Unknown'),
                        'macroarea': lang.get('Macroarea', 'Unknown'),
                        'genus': lang.get('Genus', ''),
                        'iso': lang.get('ISO639P3code', '')
                    })
                except (ValueError, TypeError):
                    pass

        return languages_with_coords
