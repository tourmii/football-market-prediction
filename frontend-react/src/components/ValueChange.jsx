import { useMemo } from 'react';
import './ValueChange.css';

/**
 * Formats a market value into a readable string (e.g., €120.5M, €850K, €15,000)
 */
function formatValue(value) {
    if (value == null) return '-';
    if (value >= 1e6) return `€${(value / 1e6).toFixed(1)}M`;
    if (value >= 1e3) return `€${(value / 1e3).toFixed(0)}K`;
    return `€${value.toLocaleString()}`;
}

/**
 * ValueChange Component
 * Displays current and previous market values with trend indicators
 * 
 * States:
 * - increase: Green with up arrow
 * - decrease: Red with down arrow  
 * - stable: Gray with dash
 */
export default function ValueChange({ currentValue, previousValue, size = 'default' }) {
    const { trend, icon, change, changePercent } = useMemo(() => {
        if (currentValue == null || previousValue == null) {
            return { trend: 'stable', icon: '−', change: 0, changePercent: 0 };
        }

        const diff = currentValue - previousValue;
        const pct = previousValue !== 0 ? ((diff / previousValue) * 100) : 0;

        if (diff > 0) {
            return {
                trend: 'increase',
                icon: '↑',
                change: diff,
                changePercent: pct.toFixed(1)
            };
        } else if (diff < 0) {
            return {
                trend: 'decrease',
                icon: '↓',
                change: Math.abs(diff),
                changePercent: Math.abs(pct).toFixed(1)
            };
        }

        return { trend: 'stable', icon: '−', change: 0, changePercent: 0 };
    }, [currentValue, previousValue]);

    return (
        <div className={`value-change value-change--${size}`}>
            <div className="value-change__current">
                {formatValue(currentValue)}
            </div>
            <div className={`value-change__previous value-change__previous--${trend}`}>
                <span className="value-change__prev-value">
                    {formatValue(previousValue)}
                </span>
                <span className={`value-change__icon value-change__icon--${trend}`}>
                    {icon}
                </span>
                {trend !== 'stable' && (
                    <span className="value-change__percent">
                        {changePercent}%
                    </span>
                )}
            </div>
        </div>
    );
}
