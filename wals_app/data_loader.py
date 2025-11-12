"""
Data loader for WALS CLDF dataset
Handles loading and querying CLDF data
"""
import os
import json
import csv
from pathlib import Path
import math

class WALSDataLoader:
    def __init__(self, cldf_path=None):
        """Initialize the data loader with CLDF dataset path"""
        if cldf_path is None:
            # Try to find cldf directory relative to app
            base_path = Path(__file__).parent.parent
            cldf_path = base_path / 'cldf'

        self.cldf_path = Path(cldf_path)
        self.data_available = self.cldf_path.exists()

        # Cache for loaded data
        self._languages = None
        self._features = None
        self._codes = None
        self._values = None
        self._contributions = None

        if self.data_available:
            self._load_data()
        else:
            self._load_sample_data()

    def _load_data(self):
        """Load data from CLDF files"""
        try:
            self._languages = self._load_csv('languages.csv')
            self._features = self._load_csv('parameters.csv')
            self._codes = self._load_csv('codes.csv')
            self._values = self._load_csv('values.csv')

            # Try to load contributions if available
            contrib_path = self.cldf_path / 'chapters.csv'
            if contrib_path.exists():
                self._contributions = self._load_csv('chapters.csv')
            else:
                self._contributions = []

        except Exception as e:
            print(f"Error loading CLDF data: {e}")
            self._load_sample_data()

    def _load_csv(self, filename):
        """Load a CSV file from CLDF directory"""
        filepath = self.cldf_path / filename
        if not filepath.exists():
            return []

        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def _load_sample_data(self):
        """Load sample data for demonstration when CLDF data is not available"""
        print("Loading sample data for demonstration...")

        # Sample languages
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

        # Sample features
        self._features = [
            {
                'ID': '81A', 'Name': 'Order of Subject, Object and Verb',
                'Chapter_ID': 's4'
            },
            {
                'ID': '1A', 'Name': 'Consonant Inventories',
                'Chapter_ID': 's1'
            },
            {
                'ID': '2A', 'Name': 'Vowel Quality Inventories',
                'Chapter_ID': 's1'
            },
        ]

        # Sample codes
        self._codes = [
            {'ID': '81A-1', 'Parameter_ID': '81A', 'Name': 'SOV', 'Number': '1'},
            {'ID': '81A-2', 'Parameter_ID': '81A', 'Name': 'SVO', 'Number': '2'},
            {'ID': '81A-3', 'Parameter_ID': '81A', 'Name': 'VSO', 'Number': '3'},
            {'ID': '1A-1', 'Parameter_ID': '1A', 'Name': 'Small', 'Number': '1'},
            {'ID': '1A-2', 'Parameter_ID': '1A', 'Name': 'Moderately small', 'Number': '2'},
            {'ID': '1A-3', 'Parameter_ID': '1A', 'Name': 'Average', 'Number': '3'},
        ]

        # Sample values
        self._values = [
            {'ID': 'eng-81A', 'Language_ID': 'eng', 'Parameter_ID': '81A', 'Code_ID': '81A-2', 'Value': '2'},
            {'ID': 'spa-81A', 'Language_ID': 'spa', 'Parameter_ID': '81A', 'Code_ID': '81A-2', 'Value': '2'},
            {'ID': 'jpn-81A', 'Language_ID': 'jpn', 'Parameter_ID': '81A', 'Code_ID': '81A-1', 'Value': '1'},
            {'ID': 'ara-81A', 'Language_ID': 'ara', 'Parameter_ID': '81A', 'Code_ID': '81A-3', 'Value': '3'},
        ]

        self._contributions = []

    def get_statistics(self):
        """Get basic statistics about the dataset"""
        return {
            'languages': len(self._languages) if self._languages else 0,
            'features': len(self._features) if self._features else 0,
            'values': len(self._values) if self._values else 0,
            'families': len(self.get_families()),
            'data_available': self.data_available
        }

    def get_detailed_statistics(self):
        """Get detailed statistics for visualization"""
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

        # Create sorted list for table display (top 20 families)
        sorted_families = sorted(family_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        stats['top_families'] = sorted_families

        return stats

    def get_languages(self, page=1, per_page=50, search='', family='', macroarea=''):
        """Get paginated list of languages with filters"""
        filtered = self._languages[:]

        # Apply filters
        if search:
            search_lower = search.lower()
            filtered = [l for l in filtered if search_lower in l.get('Name', '').lower() or
                       search_lower in l.get('ID', '').lower()]

        if family:
            filtered = [l for l in filtered if l.get('Family', '') == family]

        if macroarea:
            filtered = [l for l in filtered if l.get('Macroarea', '') == macroarea]

        # Pagination
        total = len(filtered)
        total_pages = math.ceil(total / per_page) if total > 0 else 1
        start = (page - 1) * per_page
        end = start + per_page

        return {
            'items': filtered[start:end],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        }

    def get_language(self, language_id):
        """Get a specific language by ID"""
        for lang in self._languages:
            if lang.get('ID') == language_id:
                return lang
        return None

    def get_families(self):
        """Get list of all language families"""
        families = set()
        for lang in self._languages:
            family = lang.get('Family', '')
            if family:
                families.add(family)
        return sorted(families)

    def get_macroareas(self):
        """Get list of all macroareas"""
        areas = set()
        for lang in self._languages:
            area = lang.get('Macroarea', '')
            if area:
                areas.add(area)
        return sorted(areas)

    def get_features(self, page=1, per_page=30, search='', area=''):
        """Get paginated list of features with filters"""
        filtered = self._features[:]

        # Apply filters
        if search:
            search_lower = search.lower()
            filtered = [f for f in filtered if search_lower in f.get('Name', '').lower() or
                       search_lower in f.get('ID', '').lower()]

        # Pagination
        total = len(filtered)
        total_pages = math.ceil(total / per_page) if total > 0 else 1
        start = (page - 1) * per_page
        end = start + per_page

        return {
            'items': filtered[start:end],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        }

    def get_feature(self, feature_id):
        """Get a specific feature by ID"""
        for feature in self._features:
            if feature.get('ID') == feature_id:
                return feature
        return None

    def get_areas(self):
        """Get list of all linguistic areas"""
        areas = set()
        for contrib in self._contributions:
            area = contrib.get('Area_ID', '')
            if area:
                areas.add(area)
        return sorted(areas)

    def get_codes_for_feature(self, feature_id):
        """Get all possible codes/values for a feature"""
        return [c for c in self._codes if c.get('Parameter_ID') == feature_id]

    def get_values_for_language(self, language_id):
        """Get all feature values for a specific language"""
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
        query_lower = query.lower()
        results = []
        for lang in self._languages:
            if (query_lower in lang.get('Name', '').lower() or
                query_lower in lang.get('ID', '').lower() or
                query_lower in lang.get('Family', '').lower()):
                results.append(lang)
        return results[:50]  # Limit to 50 results

    def search_features(self, query):
        """Search features by name or ID"""
        query_lower = query.lower()
        results = []
        for feature in self._features:
            if (query_lower in feature.get('Name', '').lower() or
                query_lower in feature.get('ID', '').lower()):
                results.append(feature)
        return results[:50]  # Limit to 50 results

    def get_all_languages_geo(self):
        """Get all languages with geographic coordinates for map display"""
        geo_data = []
        for lang in self._languages:
            lat = lang.get('Latitude')
            lon = lang.get('Longitude')
            if lat and lon:
                try:
                    geo_data.append({
                        'id': lang.get('ID'),
                        'name': lang.get('Name'),
                        'lat': float(lat),
                        'lon': float(lon),
                        'family': lang.get('Family', 'Unknown'),
                        'macroarea': lang.get('Macroarea', 'Unknown')
                    })
                except (ValueError, TypeError):
                    pass
        return geo_data

    def get_feature_distribution(self, feature_id):
        """Get distribution of values for a feature"""
        values = self.get_values_for_feature(feature_id)
        codes = self.get_codes_for_feature(feature_id)

        distribution = {}
        for code in codes:
            distribution[code.get('Name', 'Unknown')] = 0

        for value in values:
            code_name = value.get('Code_Name', 'Unknown')
            distribution[code_name] = distribution.get(code_name, 0) + 1

        return distribution
