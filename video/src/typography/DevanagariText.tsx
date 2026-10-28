import React from 'react';

/**
 * Devanagari is kept as intact shaped strings. If akshara-level treatment is
 * needed later, this helper's segmentation boundary is the safe place to add
 * it; individual Unicode codepoints must never be animated independently.
 */
export const DevanagariText: React.FC<{
  text: string;
  className?: string;
  style?: React.CSSProperties;
}> = ({text, className, style}) => (
  <span className={className} style={{fontFamily: 'Noto Serif Devanagari', ...style}}>
    {text}
  </span>
);
