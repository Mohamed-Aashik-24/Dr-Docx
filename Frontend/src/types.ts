export type NavItem = 'Format' | 'Analyze' | 'Train Model' | 'Settings';

export interface LogEntry {
  id: string;
  timestamp: string;
  severity: 'info' | 'success' | 'error' | 'warning';
  message: string;
}

export type ElementType = 
  | 'TITLE' | 'AUTHOR' 
  | 'CHAPTER_HEADING' | 'SECTION_HEADING' | 'SUBSECTION_HEADING' 
  | 'BODY' 
  | 'FIGURE_CAPTION' | 'TABLE_CAPTION' 
  | 'REFERENCE_HEADING' | 'REFERENCE_ENTRY' 
  | 'LIST_ITEM' 
  | 'TABLE' | 'FIGURE' 
  | 'BLANK';

export interface ClassifiedElement {
  id: string;
  type: ElementType;
  source: 'rule' | 'ml' | 'context';
  text: string;
}

export interface Settings {
  font: string;
  lineSpacing: number;
  marginTop: number;
  marginBottom: number;
  marginLeft: number;
  marginRight: number;
}
