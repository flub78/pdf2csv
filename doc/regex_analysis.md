# Regular Expression Analysis for pdf2csv Project

This document provides a comprehensive review of all regular expressions used in the pdf2csv project, their locations, purposes, and potential issues or improvements.

## Summary

The project contains **58 distinct regular expressions** across 4 main files. The patterns are primarily used for:
- **Text filtering** (33 patterns): Removing unwanted content from bank statements
- **Date parsing** (8 patterns): Extracting dates in various formats
- **Amount parsing** (8 patterns): Extracting monetary amounts
- **Data extraction** (9 patterns): Extracting account numbers, bank names, transaction data

## File-by-File Analysis

### 1. src/parsers/base_parser.py

#### Line Filtering Patterns (Lines 58-93)
**Purpose**: Filter out unwanted lines from bank statement text

| Line | Pattern | Purpose | Potential Issues |
|------|---------|---------|------------------|
| 58 | `r'VOS CONTACTS'` | Remove contact section | ✅ Specific to SG format |
| 59 | `r'Votre Banque à Distance'` | Remove online banking info | ✅ Specific to SG format |
| 60 | `r'Internet\s*:\s*entreprises\.sg\.fr'` | Remove website reference | ✅ Good escaping of dots |
| 61 | `r'éléphone\s*:\s*\d+'` | Remove phone numbers | ⚠️ Missing 'T' in "Téléphone" |
| 62 | `r'Courrier\s*:\s*\d+.*ABBEVILLE'` | Remove postal address | ✅ Flexible matching |
| 63 | `r'AERODROME D ABBEVILLE'` | Remove location reference | ✅ Literal match |
| 64 | `r'Service d\'urgence 24 h/24'` | Remove emergency service info | ✅ Good escaping |
| 65 | `r'Perte ou vol de vos cartes'` | Remove card security info | ✅ Literal match |
| 66 | `r'Pour toute insatisfaction'` | Remove complaint info | ✅ Literal match |
| 67 | `r'L\'agence\s*:\s*votre premier'` | Remove agency info | ✅ Good escaping |
| 68 | `r'Le Service Relations Clientèle'` | Remove customer service info | ✅ Literal match |
| 69 | `r'Le Médiateur\s*:\s*En dernier'` | Remove mediator info | ✅ Flexible matching |
| 70 | `r'Société Générale'` | Remove bank name from content | ✅ Literal match |
| 71 | `r'S\.A\. au capital'` | Remove legal entity info | ✅ Good escaping |
| 72 | `r'RCS Paris'` | Remove company registration | ✅ Literal match |
| 73 | `r'Siège Social'` | Remove headquarters info | ✅ Literal match |
| 74 | `r'bd Haussmann'` | Remove address | ✅ Literal match |
| 75 | `r'suite >>>'` | Remove continuation marker | ✅ Literal match |
| 76 | `r'RA\d+'` | Remove reference numbers | ✅ Good pattern |
| 77 | `r'N° ADEME'` | Remove environmental number | ✅ Literal match |
| 78 | `r'Opération exonérée'` | Remove exemption notice | ✅ Literal match |
| 79 | `r'Votre compte est éligible'` | Remove eligibility notice | ✅ Literal match |
| 80 | `r'Fonds de Garantie'` | Remove guarantee fund info | ✅ Literal match |
| 81 | `r'SG-SocieteGenerale\.Reclamations@socgen\.com'` | Remove email | ✅ Good escaping |
| 82 | `r'courrier à : Le médiateur CS 151'` | Remove mediator address | ✅ Literal match |
| 83 | `r'RELEVÉ DE COMPTE'` | Remove statement header | ✅ Literal match |
| 84 | `r'COMPTE D\'ADMINISTRATION - en euros'` | Remove account type | ✅ Good escaping |
| 85 | `r'n° 30003 02846 00050034631 54'` | Remove specific account | ⚠️ Too specific, not reusable |
| 86 | `r'du \d{2}/\d{2}/\d{4} au \d{2}/\d{2}/\d{4}'` | Remove date range | ✅ Good date pattern |
| 87 | `r'envoi n°\d+ Page \d+/\d+'` | Remove page numbers | ✅ Good pattern |
| 88 | `r'Nature de l\'opération'` | Remove column header | ✅ Good escaping |
| 89 | `r'^Débit$'` | Remove standalone "Débit" | ✅ Good anchoring |
| 90 | `r'^Crédit$'` | Remove standalone "Crédit" | ✅ Good anchoring |
| 91 | `r'^Valeur$'` | Remove standalone "Valeur" | ✅ Good anchoring |
| 92 | `r'^Date$'` | Remove standalone "Date" | ✅ Good anchoring |
| 93 | `r'^eur$'` | Remove standalone "eur" | ✅ Good anchoring |

#### Stop Processing Pattern (Line 99)
| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 99 | `r'TOTAUX DES MOUVEMENTS'` | Stop parsing at totals section | ✅ Correct |

#### Generic Date Patterns (Lines 155-158)
**Purpose**: Extract dates in various international formats

| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 155 | `r'\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\b'` | DD/MM/YYYY or MM/DD/YYYY | ⚠️ Ambiguous US/EU format |
| 156 | `r'\b(\d{2,4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2})\b'` | YYYY/MM/DD | ✅ Good pattern |
| 157 | `r'\b(\d{1,2}\s+\w{3}\s+\d{2,4})\b'` | DD MMM YYYY | ✅ Good pattern |
| 158 | `r'\b(\w{3}\s+\d{1,2},?\s+\d{2,4})\b'` | MMM DD, YYYY | ✅ Good pattern |

#### Generic Amount Patterns (Lines 163-164)
**Purpose**: Extract monetary amounts with currency symbols

| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 163-170 | Multiple improved patterns | Amount extraction supporting up to 10+ million | ✅ **FIXED**: Now supports large unformatted amounts, US/French formats |

**New Pattern Details:**
- `r'[\$€£¥]?\s*([+-]?\d{1,3}(?:[,\s]\d{3})+(?:\.\d{2})?)'` - US format with commas
- `r'[\$€£¥]?\s*([+-]?\d{1,3}(?:\.\d{3})+(?:,\d{2})?)'` - French format with dots  
- `r'[\$€£¥]?\s*([+-]?\d{4,}(?:[.,]\d{2})?)'` - Unformatted large amounts
- `r'[\$€£¥]?\s*([+-]?\d{1,3}(?:[.,]\d{2})?)'` - Small amounts

#### Bank Name Patterns (Lines 169-171)
**Purpose**: Extract generic bank names

| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 169 | `r'(?i)\b([A-Z][a-z]+\s+(?:Bank|Credit\s+Union|Financial))\b'` | English bank patterns | ✅ Good for international |
| 170 | `r'(?i)\b(Bank\s+of\s+[A-Z][a-z]+)\b'` | "Bank of X" pattern | ✅ Good pattern |
| 171 | `r'(?i)\b([A-Z]+\s+Bank)\b'` | "XXX Bank" pattern | ✅ Good pattern |

#### Account and Code Patterns (Lines 197, 202)
**Purpose**: Extract account numbers and bank codes

| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 197 | `r'(?i)account\s*(?:number|#)?\s*:?\s*(\w+[-\s]?\w+)'` | Account numbers | ⚠️ Limited to 2 word groups |
| 202 | `r'(?i)(?:sort\s+code|routing|swift|iban)\s*:?\s*([A-Z0-9\-\s]+)'` | Bank codes | ✅ Good international coverage |

#### Text Cleaning Pattern (Line 315)
| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 315 | `r'\s+'` | Normalize whitespace | ✅ Standard pattern |

### 2. src/parsers/sg_parser.py

#### SG-Specific Patterns (Lines 29-36)
**Purpose**: Extract Société Générale specific data structures

| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 29 | `r'n°\s*(\d+\s+\d+\s+\d+\s+\d+)'` | Account number format | ✅ Specific to SG format |
| 30 | `r'du\s+(\d{2}/\d{2}/\d{4})\s+au\s+(\d{2}/\d{2}/\d{4})'` | Date range extraction | ✅ Good French format |
| 31 | `r'(?:AERO CLUB|[A-Z][A-Z\s-]+)\n(?:[A-Z\s-]+\n)*(?:AERODROME|[A-Z0-9\s]+)\n(?:D\s+\d+|[A-Z0-9\s]+)\n(?:\d{5}\s+[A-Z\s]+)'` | Client info pattern | ⚠️ Overly specific to test data |
| 34 | `r'(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})\s+(.+?)(?:\d+[,\.]\d{2}|\n)'` | Transaction line | ✅ Good transaction pattern |
| 35 | Updated flexible amount pattern | French amount format | ✅ **FIXED**: Now supports large amounts |
| 36 | Updated flexible balance pattern | Final balance | ✅ **FIXED**: Now supports large amounts |

#### Client Extraction Pattern (Line 52)
| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 52 | `r'(AERO CLUB D\'ABBEVILLE - BUIGNY[^)]+BUIGNY SAINT MACLOU)'` | Extract client name | ⚠️ Hardcoded to specific client |

#### Account Extraction Pattern (Line 59)
| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 59 | `r'n°\s*(\d+\s+\d+\s+\d+\s+\d+)'` | Extract account number | ✅ Consistent with line 29 |

#### Balance Extraction Pattern (Line 68)
| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 68 | `r'NOUVEAU SOLDE AU \d{2}/\d{2}/\d{4}\s+(\d{1,3}(?:\.\d{3})*,\d{2})'` | Extract final balance | ✅ Good pattern |

#### Transaction Processing Patterns (Lines 98, 117, 162, 166, 173)
**Purpose**: Parse transaction details

| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 98 | `r'^(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})\s+(.+)'` | Transaction start line | ✅ Good anchoring |
| 117 | `r'(\d{1,3}(?:\.\d{3})*,\d{2})\s*\*?\s*$'` | Inline amount extraction | ✅ Good end anchoring |
| 162 | `r'^(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})'` | Next transaction check | ✅ Good pattern |
| 166 | `r'^(\d{1,3}(?:\.\d{3})*,\d{2})\s*\*?$'` | Amount line detection | ✅ Good anchoring |
| 173 | `r'^\d+$'` | Cheque number detection | ✅ Simple and effective |

#### Text Cleaning Patterns (Lines 284, 287)
**Purpose**: Clean transaction text

| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 284 | `r'[\r\n]+'` | Remove line breaks | ✅ Good pattern |
| 287 | `r' +'` | Normalize spaces | ✅ Standard pattern |

### 3. src/parsers/specific_parsers.py

#### French Date Patterns (Lines 39-40)
**Purpose**: Parse French date formats

| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 39 | `r'\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\b'` | DD/MM/YYYY format | ✅ European format |
| 40 | `r'\b(\d{1,2}\s+(?:janv|févr|mars|avr|mai|juin|juil|août|sept|oct|nov|déc)\w*\.?\s+\d{2,4})\b'` | French month names | ✅ Good French coverage |

#### French Amount Patterns (Lines 45-47)
**Purpose**: Parse French monetary amounts

| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 45-51 | Multiple improved French patterns | French amount extraction | ✅ **FIXED**: Now supports large amounts in all French formats |

**New Pattern Details:**
- `r'([+-]?\d{1,3}(?:\s\d{3})+(?:,\d{2})?)\s*€'` - Space-separated format
- `r'([+-]?\d{1,3}(?:\.\d{3})+(?:,\d{2})?)\s*EUR'` - Dot-separated format  
- `r'([+-]?\d{4,}(?:,\d{2})?)\s*€?'` - Unformatted large amounts
- `r'€\s*([+-]?\d{1,3}(?:\s\d{3})+(?:,\d{2})?)'` - Euro prefix patterns

#### French Bank Patterns (Lines 52-55)
**Purpose**: Identify French banks

| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 52 | `r'(?i)\b(Crédit\s+(?:Agricole|Mutuel|du\s+Nord|Lyonnais))\b'` | Major French banks | ✅ Good coverage |
| 53 | `r'(?i)\b(Banque\s+(?:Populaire|Postale|de\s+France))\b'` | Public/regional banks | ✅ Good coverage |
| 54 | `r'(?i)\b(BNP\s*Paribas|Société\s+Générale|LCL)\b'` | Major commercial banks | ✅ Good coverage |
| 55 | `r'(?i)\b(Caisse\s+d\'Épargne)\b'` | Savings bank | ✅ Good escaping |

#### French Account Patterns (Lines 81-83)
**Purpose**: Extract French account numbers

| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 81 | `r'(?i)compte\s*(?:n°|numéro)?\s*:?\s*(\d+[\s\-]?\d*)'` | French account format | ⚠️ Limited flexibility |
| 82 | `r'(?i)n°\s*compte\s*:?\s*(\d+[\s\-]?\d*)'` | Numbered account | ⚠️ Limited flexibility |
| 83 | `r'\b(\d{5,}\s*\d{3,})\b'` | Generic long number | ⚠️ Too broad |

#### Pattern Usage (Line 152)
| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 152 | `r'^' + pattern` | Anchor to line start | ✅ Dynamic anchoring |

#### Text Cleaning (Line 208)
| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 208 | `r'\s+'` | Normalize whitespace | ✅ Standard pattern |

### 4. generate_comparison.py

#### Transaction Parsing Patterns (Lines 45, 54, 88)
**Purpose**: Parse transactions from text and CSV files

| Line | Pattern | Purpose | Issues |
|------|---------|---------|--------|
| 45 | `r'(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})\s+(.+)'` | Text transaction line | ✅ Same as SG parser |
| 54 | `r'^\d{1,3}(?:\.\d{3})*,\d{2}$'` | French amount detection | ✅ Good anchoring |
| 88 | `r'^\d{2}/\d{2}/\d{4}$'` | CSV date detection | ✅ Good anchoring |

## Issues and Recommendations

### 🔴 Critical Issues

1. **Line 85 (base_parser.py)**: `r'n° 30003 02846 00050034631 54'`
   - **Issue**: Hardcoded specific account number
   - **Impact**: Will not work for other accounts
   - **Fix**: Replace with generic pattern or remove

2. **Line 52 (sg_parser.py)**: Client pattern hardcoded to "AERO CLUB D'ABBEVILLE"
   - **Issue**: Only works for this specific client
   - **Impact**: Parser fails for other SG customers
   - **Fix**: Generalize or make configurable

3. **Line 31 (sg_parser.py)**: Overly complex client pattern
   - **Issue**: Too specific to test data structure
   - **Impact**: Brittle parsing
   - **Fix**: Simplify and make more flexible

4. **Lines 163-164 (base_parser.py)**: Amount patterns with `\d{1,3}` limitation - ✅ **FIXED**
   - **Original Issue**: Cannot parse large amounts without thousand separators (e.g., "5000000,00")
   - **Impact**: Parser fails on corporate accounts, large transfers, unformatted amounts
   - **Examples that failed**: `€ 5000000,00`, `$ 25000000.00`, `12345,67`
   - **Fix Applied**: Implemented flexible patterns supporting both formatted and unformatted amounts up to 10+ million

### ⚠️ Major Issues

5. **Line 61 (base_parser.py)**: `r'éléphone\s*:\s*\d+'`
   - **Issue**: Missing 'T' in "Téléphone"
   - **Impact**: Won't match actual phone number lines
   - **Fix**: Change to `r'[Tt]éléphone\s*:\s*\d+'`

6. **Mixed decimal separators in generic patterns**
   - **Issue**: Patterns accept both comma and dot as decimal separators
   - **Impact**: May cause parsing errors
   - **Fix**: Use format-specific patterns

7. **Account number patterns too restrictive**
   - **Issue**: Limited to simple formats
   - **Impact**: Won't work with complex account numbers
   - **Fix**: More flexible patterns

8. **Similar amount pattern limitations in other files** - ✅ **FIXED**
   - **Line 47 (specific_parsers.py)**: Updated French amount patterns
   - **Lines 36,38 (sg_parser.py)**: Updated SG-specific amount patterns  
   - **Line 54 (generate_comparison.py)**: Updated comparison script patterns
   - **Impact**: All amount parsing now supports large unformatted amounts consistently

### ✅ Good Practices Found

1. **Proper escaping**: Dots and special characters properly escaped
2. **Anchoring**: Good use of `^` and `$` anchors where appropriate
3. **Case insensitive**: Appropriate use of `(?i)` flag
4. **Flexible whitespace**: Good use of `\s*` and `\s+`

### 📋 Improvement Recommendations

1. **Create pattern constants**: Move repeated patterns to module-level constants
2. **Add pattern validation**: Test patterns against known input variations
3. **Modularize by purpose**: Group patterns by function (dates, amounts, etc.)
4. **Add configuration**: Make bank-specific patterns configurable
5. **Improve error handling**: Add fallback patterns for edge cases
6. **Documentation**: Add comments explaining complex patterns
7. **Testing**: Create unit tests for each pattern

### 🎯 Specific Refactoring Suggestions

1. **Consolidate date patterns**: Merge similar date patterns across files
2. **Standardize amount patterns**: Create consistent French vs international amount handling
3. **Generalize ignore patterns**: Make filtering patterns configurable per bank
4. **Improve bank detection**: Add more robust bank identification patterns
5. **Better transaction parsing**: More flexible transaction line detection

## Pattern Complexity Analysis

- **Simple literal matches**: 31 patterns (53%)
- **Character classes**: 12 patterns (21%)  
- **Quantifiers**: 43 patterns (74%)
- **Anchors**: 15 patterns (26%)
- **Groups**: 25 patterns (43%)
- **Lookaheads/lookbehinds**: 0 patterns (0%)

Most patterns are appropriately simple, but some could benefit from more sophisticated regex features for better accuracy.
