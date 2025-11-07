import { useState, useEffect, useRef, useCallback } from 'react';
import { t } from '../i18n';
import { translateMaterialName } from '../translations';

interface MaterialSelectorProps {
  materials: string[];
  selectedMaterial: string;
  onMaterialChange: (material: string) => void;
  language?: 'de' | 'en';
  onLiveSearch?: (query: string) => void;
}

// Fuzzy search function - finds matches even with typos
function fuzzyMatch(query: string, text: string): { score: number; matched: boolean } {
  const queryLower = query.toLowerCase();
  const textLower = text.toLowerCase();
  
  // Exact match gets highest score
  if (textLower === queryLower) return { score: 100, matched: true };
  
  // Starts with query
  if (textLower.startsWith(queryLower)) return { score: 80, matched: true };
  
  // Contains query
  if (textLower.includes(queryLower)) return { score: 60, matched: true };
  
  // Fuzzy match (characters in order)
  let queryIndex = 0;
  for (let i = 0; i < textLower.length && queryIndex < queryLower.length; i++) {
    if (textLower[i] === queryLower[queryIndex]) {
      queryIndex++;
    }
  }
  
  if (queryIndex === queryLower.length) {
    return { score: 40, matched: true };
  }
  
  return { score: 0, matched: false };
}

// Highlight matching text
function highlightMatch(text: string, query: string): React.ReactNode {
  if (!query) return <>{text}</>;
  
  const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
  const parts = text.split(regex);
  
  return (
    <>
      {parts.map((part, index) =>
        regex.test(part) ? (
          <mark key={index} className="bg-orange-500/30 text-orange-200 px-1 rounded">
            {part}
          </mark>
        ) : (
          <span key={index}>{part}</span>
        )
      )}
    </>
  );
}

export default function MaterialSelector({
  materials,
  selectedMaterial,
  onMaterialChange,
  language = 'de',
  onLiveSearch,
}: MaterialSelectorProps) {
  const [inputValue, setInputValue] = useState(selectedMaterial);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);
  const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Debounced live search - zeigt Items während des Tippens
  // WICHTIG: Wählt nur automatisch aus wenn es EINDEUTIG ist (exaktes Match oder nur 1 Match)
  const debouncedLiveSearch = useCallback((query: string) => {
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    
    debounceTimerRef.current = setTimeout(() => {
      if (onLiveSearch && query.length >= 2) {
        // 1. Exaktes Match (höchste Priorität)
        const exactMatch = materials.find(m => 
          m.toLowerCase() === query.toLowerCase() ||
          translateMaterialName(m, language).toLowerCase() === query.toLowerCase()
        );
        if (exactMatch) {
          onLiveSearch(exactMatch);
          return;
        }
        
        // 2. Finde ALLE Matches die mit Query beginnen
        const startsWithMatches = materials.filter(m => {
          const translated = translateMaterialName(m, language).toLowerCase();
          const original = m.toLowerCase();
          return translated.startsWith(query.toLowerCase()) || 
                 original.startsWith(query.toLowerCase());
        });
        
        // Nur automatisch auswählen wenn es GENAU 1 Match gibt
        if (startsWithMatches.length === 1) {
          onLiveSearch(startsWithMatches[0]);
          return;
        }
        
        // 3. Wenn mehrere Matches: Zeige nur im Dropdown, wähle NICHT automatisch
        // (Der User muss explizit auswählen)
      }
    }, 300); // 300ms delay
  }, [materials, language, onLiveSearch]);

  // Improved fuzzy search with better sorting
  const filteredSuggestions = materials
    .map(material => {
      const translated = translateMaterialName(material, language);
      const originalMatch = fuzzyMatch(inputValue, material);
      const translatedMatch = fuzzyMatch(inputValue, translated);
      
      // Use the better match score
      const score = Math.max(originalMatch.score, translatedMatch.score);
      const matched = originalMatch.matched || translatedMatch.matched;
      
      return {
        material,
        translated,
        score,
        matched,
      };
    })
    .filter(item => item.matched)
    .sort((a, b) => b.score - a.score) // Higher score first
    .slice(0, 15) // Show more suggestions
    .map(item => item.material);

  useEffect(() => {
    setInputValue(selectedMaterial);
  }, [selectedMaterial]);

  const handleInputChange = (value: string) => {
    // Sanitize input: limit length and remove potentially dangerous characters
    const sanitized = value.slice(0, 100).replace(/[<>\"']/g, '');
    setInputValue(sanitized);
    setShowSuggestions(true);
    
    // Live Search: Während des Tippens automatisch Items suchen
    if (onLiveSearch) {
      debouncedLiveSearch(sanitized);
    } else {
      // Normales Verhalten: nur bei Auswahl updaten
      onMaterialChange(sanitized);
    }
  };

  // Auto-highlight wenn nur 1 Suggestion (wie moderne Autocompletes)
  useEffect(() => {
    if (showSuggestions && filteredSuggestions.length === 1) {
      setHighlightedIndex(0);
    } else if (filteredSuggestions.length > 1) {
      // Reset highlight wenn mehrere Matches
      setHighlightedIndex(-1);
    }
  }, [filteredSuggestions.length, showSuggestions]);

  const handleSuggestionClick = (material: string) => {
    setInputValue(material);
    setShowSuggestions(false);
    setHighlightedIndex(-1);
    onMaterialChange(material);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    // Wenn keine Suggestions: Tab/Enter normal verwenden
    if (!showSuggestions || filteredSuggestions.length === 0) {
      // Tab: Normal behavior (navigate away)
      if (e.key === 'Tab') {
        return; // Allow default Tab behavior
      }
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setHighlightedIndex(prev => 
          prev < filteredSuggestions.length - 1 ? prev + 1 : prev
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setHighlightedIndex(prev => (prev > 0 ? prev - 1 : -1));
        break;
      case 'Enter':
      case 'Tab':
        e.preventDefault();
        // Wenn nur 1 Match oder highlighted → auswählen
        if (filteredSuggestions.length === 1) {
          handleSuggestionClick(filteredSuggestions[0]);
        } else if (highlightedIndex >= 0 && highlightedIndex < filteredSuggestions.length) {
          handleSuggestionClick(filteredSuggestions[highlightedIndex]);
        } else if (highlightedIndex === -1 && filteredSuggestions.length > 0) {
          // Wenn nichts highlighted aber Suggestions da → erstes auswählen
          handleSuggestionClick(filteredSuggestions[0]);
        }
        break;
      case 'Escape':
        e.preventDefault();
        setShowSuggestions(false);
        setHighlightedIndex(-1);
        inputRef.current?.blur();
        break;
    }
  };

  // Scroll highlighted item into view
  useEffect(() => {
    if (highlightedIndex >= 0 && suggestionsRef.current) {
      const highlightedElement = suggestionsRef.current.children[highlightedIndex] as HTMLElement;
      if (highlightedElement) {
        highlightedElement.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    }
  }, [highlightedIndex]);

  return (
    <div className="relative">
      <label className="block text-sm font-semibold mb-2">{t('materialInput', language)}</label>
      <input
        ref={inputRef}
        type="text"
        value={inputValue}
        onChange={(e) => handleInputChange(e.target.value)}
        onFocus={() => {
          setShowSuggestions(true);
          // Live Search auch beim Focus wenn schon Text da ist
          if (onLiveSearch && inputValue.length >= 2) {
            debouncedLiveSearch(inputValue);
          }
        }}
        onBlur={() => {
          // Delay to allow click events
          setTimeout(() => {
            setShowSuggestions(false);
            setHighlightedIndex(-1);
          }, 200);
        }}
        onKeyDown={handleKeyDown}
        placeholder={t('materialPlaceholder', language)}
        className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:border-orange-500 text-white placeholder-gray-400"
      />
      {onLiveSearch && inputValue.length >= 2 && (
        <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
         
        </div>
      )}
      {showSuggestions && inputValue && filteredSuggestions.length > 0 && (
        <div
          ref={suggestionsRef}
          className="absolute z-20 w-full mt-1 bg-gray-800 border border-gray-700 rounded-lg shadow-lg max-h-60 overflow-y-auto"
        >
          {filteredSuggestions.map((material, index) => {
            const translated = translateMaterialName(material, language);
            const isHighlighted = index === highlightedIndex;
            
            return (
              <button
                key={material}
                onClick={() => handleSuggestionClick(material)}
                className={`w-full text-left px-4 py-2 text-sm transition-colors ${
                  isHighlighted
                    ? 'bg-orange-500/20 text-orange-200'
                    : 'hover:bg-gray-700 text-gray-200'
                }`}
              >
                {highlightMatch(translated, inputValue)}
                {material !== translated && (
                  <span className="text-xs text-gray-500 ml-2">({material})</span>
                )}
              </button>
            );
          })}
        </div>
      )}
      {showSuggestions && inputValue && filteredSuggestions.length === 0 && (
        <div className="absolute z-20 w-full mt-1 bg-gray-800 border border-gray-700 rounded-lg shadow-lg p-4 text-sm text-gray-400 text-center">
          Keine Materialien gefunden
        </div>
      )}
    </div>
  );
}
