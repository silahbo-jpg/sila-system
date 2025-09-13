"""
i18n Middleware and Translation System for SILA

This module provides comprehensive internationalization support with:
- Automatic language detection from Accept-Language header
- User profile language preferences
- Dynamic translation loading
- Fallback language support
"""

import json
import os
from typing import Dict, Optional, List, Any
from pathlib import Path
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class TranslationManager:
    """Manages translations and language detection"""
    
    def __init__(self, translations_dir: Path):
        self.translations_dir = translations_dir
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.supported_languages = ['pt', 'en', 'fr', 'es']  # Portuguese, English, French, Spanish
        self.default_language = 'pt'
        self.fallback_language = 'en'
        
        # Ensure translations directory exists
        translations_dir.mkdir(parents=True, exist_ok=True)
        
        # Load all available translations
        self.load_translations()
        
    def load_translations(self):
        """Load all translation files from the translations directory"""
        for lang in self.supported_languages:
            translation_file = self.translations_dir / f"{lang}.json"
            if translation_file.exists():
                try:
                    with open(translation_file, 'r', encoding='utf-8') as f:
                        self.translations[lang] = json.load(f)
                    logger.info(f"Loaded translations for language: {lang}")
                except Exception as e:
                    logger.error(f"Error loading translations for {lang}: {str(e)}")
                    self.translations[lang] = {}
            else:
                self.translations[lang] = {}
                
    def save_translations(self, lang: str):
        """Save translations for a specific language"""
        translation_file = self.translations_dir / f"{lang}.json"
        try:
            with open(translation_file, 'w', encoding='utf-8') as f:
                json.dump(self.translations[lang], f, ensure_ascii=False, indent=2)
            logger.info(f"Saved translations for language: {lang}")
        except Exception as e:
            logger.error(f"Error saving translations for {lang}: {str(e)}")
            
    def get_translation(self, key: str, lang: str, fallback: str = None) -> str:
        """
        Get translation for a key in specified language
        
        Args:
            key: Translation key (e.g., 'services.health.agendamento_consulta.name')
            lang: Target language code
            fallback: Fallback text if translation not found
            
        Returns:
            Translated text or fallback
        """
        # Try requested language
        if lang in self.translations:
            value = self._get_nested_value(self.translations[lang], key)
            if value:
                return value
                
        # Try fallback language
        if self.fallback_language in self.translations:
            value = self._get_nested_value(self.translations[self.fallback_language], key)
            if value:
                return value
                
        # Return fallback text or key
        return fallback or key
        
    def _get_nested_value(self, data: Dict, key: str) -> Optional[str]:
        """Get nested dictionary value using dot notation"""
        keys = key.split('.')
        current = data
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return None
                
        return str(current) if current is not None else None
        
    def set_translation(self, key: str, lang: str, value: str):
        """Set translation for a key in specified language"""
        keys = key.split('.')
        current = self.translations.setdefault(lang, {})
        
        # Navigate to the nested location
        for k in keys[:-1]:
            current = current.setdefault(k, {})
            
        # Set the value
        current[keys[-1]] = value
        
    def detect_language(self, request: Request, user_lang: str = None) -> str:
        """
        Detect user's preferred language
        
        Priority:
        1. User profile language (if provided)
        2. Accept-Language header
        3. Default language
        """
        # Priority 1: User profile language
        if user_lang and user_lang in self.supported_languages:
            return user_lang
            
        # Priority 2: Accept-Language header
        accept_language = request.headers.get('Accept-Language', '')
        if accept_language:
            # Parse Accept-Language header
            languages = []
            for lang_range in accept_language.split(','):
                parts = lang_range.strip().split(';')
                lang = parts[0].strip()
                
                # Extract just the language code (ignore country)
                lang_code = lang.split('-')[0].lower()
                
                if lang_code in self.supported_languages:
                    # Parse quality factor (q value)
                    quality = 1.0
                    if len(parts) > 1:
                        for part in parts[1:]:
                            if part.strip().startswith('q='):
                                try:
                                    quality = float(part.strip()[2:])
                                except ValueError:
                                    quality = 1.0
                    languages.append((lang_code, quality))
                    
            # Sort by quality and return highest
            if languages:
                languages.sort(key=lambda x: x[1], reverse=True)
                return languages[0][0]
                
        # Priority 3: Default language
        return self.default_language
        
    def translate_response(self, response_data: Any, lang: str) -> Any:
        """
        Recursively translate response data
        
        Looks for keys ending with '_pt' or '_en' and returns appropriate language
        """
        if isinstance(response_data, dict):
            translated = {}
            for key, value in response_data.items():
                # Handle bilingual fields
                if key.endswith('_pt') and lang == 'pt':
                    base_key = key[:-3]  # Remove '_pt'
                    translated[base_key] = value
                elif key.endswith('_en') and lang == 'en':
                    base_key = key[:-3]  # Remove '_en'
                    translated[base_key] = value
                elif key.endswith('_pt') and lang != 'pt':
                    # Skip Portuguese version if not requested
                    continue
                elif key.endswith('_en') and lang != 'en':
                    # Skip English version if not requested
                    continue
                else:
                    # Recursively translate nested objects
                    translated[key] = self.translate_response(value, lang)
            return translated
            
        elif isinstance(response_data, list):
            return [self.translate_response(item, lang) for item in response_data]
            
        return response_data

# Global translation manager
translation_manager: Optional[TranslationManager] = None

def initialize_translations(translations_dir: Path):
    """Initialize the global translation manager"""
    global translation_manager
    translation_manager = TranslationManager(translations_dir)
    logger.info(f"Translation system initialized with directory: {translations_dir}")

async def i18n_middleware(request: Request, call_next):
    """
    FastAPI middleware for automatic internationalization
    
    This middleware:
    1. Detects user's preferred language
    2. Sets language in request state
    3. Translates responses automatically
    """
    # Detect language
    user_lang = None  # TODO: Get from user profile when auth is available
    
    if translation_manager:
        detected_lang = translation_manager.detect_language(request, user_lang)
        request.state.language = detected_lang
    else:
        request.state.language = 'pt'  # Default
        
    # Process request
    response = await call_next(request)
    
    # Translate response if it's JSON
    if (hasattr(response, 'media_type') and 
        response.media_type == 'application/json' and
        translation_manager):
        
        # Get response body
        if hasattr(response, 'body'):
            try:
                import json
                response_data = json.loads(response.body.decode())
                translated_data = translation_manager.translate_response(
                    response_data, 
                    request.state.language
                )
                
                # Create new response with translated data
                return JSONResponse(
                    content=translated_data,
                    status_code=response.status_code,
                    headers=dict(response.headers)
                )
            except Exception as e:
                logger.warning(f"Error translating response: {str(e)}")
                
    # Add language headers
    if hasattr(request.state, 'language'):
        response.headers["Content-Language"] = request.state.language
        
    return response

def get_current_language(request: Request) -> str:
    """Get the current request language"""
    return getattr(request.state, 'language', 'pt')

def translate(key: str, request: Request = None, lang: str = None, fallback: str = None) -> str:
    """
    Translate a key to the current or specified language
    
    Args:
        key: Translation key
        request: Current request (to get language)
        lang: Specific language (overrides request language)
        fallback: Fallback text
        
    Returns:
        Translated text
    """
    if not translation_manager:
        return fallback or key
        
    # Determine language
    if lang:
        target_lang = lang
    elif request and hasattr(request.state, 'language'):
        target_lang = request.state.language
    else:
        target_lang = 'pt'
        
    return translation_manager.get_translation(key, target_lang, fallback)

# Helper function for template translations
def t(key: str, **kwargs) -> str:
    """Short alias for translate function (template-friendly)"""
    # This would be used in templates: {{ t('services.health.name') }}
    if translation_manager:
        lang = kwargs.get('lang', 'pt')
        return translation_manager.get_translation(key, lang, kwargs.get('fallback', key))
    return key