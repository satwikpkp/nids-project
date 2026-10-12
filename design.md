# Design System & UI Specification

## 1. Aesthetic Direction: Futuristic SOC & Cyber Defense
The visual identity of the **Adaptive Lightweight NIDS Dashboard** is inspired by modern Security Operations Centers (SOC) and mission-critical telemetry interfaces. It utilizes a **deep dark mode palette**, subtle glassmorphic panels, glowing status indicators, and high-legibility monospace accents for network data.

---

## 2. Color Palette & Theme Tokens

### 2.1. Backgrounds & Surfaces
- **App Background (Deep Void)**: `#0B0F17` (Rich, deep midnight black-blue)
- **Card / Surface Dark**: `#111827` (Tailwind `slate-900` / deep charcoal)
- **Elevated Surface (Glassmorphism)**: `rgba(17, 24, 39, 0.75)` with `backdrop-filter: blur(12px)`
- **Border / Divider**: `rgba(255, 255, 255, 0.08)` or `#1E293B` (`slate-800`)
- **Hover / Active State**: `#1E293B` with border highlight `rgba(59, 130, 246, 0.3)`

### 2.2. Cyber Accents & Primary Brand Colors
- **Primary Cyber Cyan**: `#06B6D4` (`cyan-500`) / Glow: `rgba(6, 182, 212, 0.35)`
- **Electric Blue (Action / Focus)**: `#3B82F6` (`blue-500`)
- **Neon Purple (Ensemble / AI)**: `#8B5CF6` (`violet-500`)
- **Emerald Green (Normal / Secure)**: `#10B981` (`emerald-500`) / Glow: `rgba(16, 185, 129, 0.3)`
- **Amber Gold (Warning / Suspicious)**: `#F59E0B` (`amber-500`)
- **Crimson Red (Critical Threat / Under Attack)**: `#EF4444` (`red-500`) / Glow: `rgba(239, 68, 68, 0.4)`
- **Violet Accent (Unknown / Zero-Day Anomaly)**: `#EC4899` (`pink-500`)

### 2.3. Text & Typography Colors
- **Text Primary (High Contrast)**: `#F9FAFB` (`gray-50`)
- **Text Secondary (Subtle Info)**: `#94A3B8` (`slate-400`)
- **Text Muted (Captions / Disabled)**: `#64748B` (`slate-500`)
- **Text Accent (Interactive)**: `#38BDF8` (`sky-400`)

---

## 3. Typography & Font Hierarchy

### 3.1. Font Families
- **Primary Interface Font**: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
  - *Usage*: Navigation, buttons, headings, analytics descriptions, metric labels.
  - *Characteristics*: Modern, neutral, extremely legible at small sizes.
- **Data & Telemetry Font (Monospace)**: `'JetBrains Mono', 'Fira Code', 'Courier New', monospace`
  - *Usage*: IP addresses, MAC addresses, port numbers, packet hashes, timestamps, latency (ms), confidence scores.
  - *Characteristics*: Tabular numbers alignment, distinct digit shapes, tactical cyber aesthetic.

### 3.2. Type Scale & Hierarchy

| Level | Size | Weight | Line Height | Tracking | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **H1 (Page Title)** | `28px` (`1.75rem`) | `700` (Bold) | `36px` | `-0.02em` | Main dashboard & login header |
| **H2 (Section Header)**| `20px` (`1.25rem`) | `600` (SemiBold) | `28px` | `-0.01em` | Panel & card titles |
| **H3 (Sub-heading)**   | `16px` (`1.0rem`)  | `600` (SemiBold) | `24px` | `0` | Sub-sections, modal headers |
| **KPI Metric Value**  | `32px` (`2.0rem`)  | `800` (ExtraBold)| `38px` | `-0.03em` | Primary statistical figures |
| **Body (Default)**    | `14px` (`0.875rem`)| `400` (Regular)  | `20px` | `0` | Descriptions, list items |
| **Body Small / Captions**| `12px` (`0.75rem`) | `500` (Medium)   | `16px` | `0.01em` | Table headers, metadata |
| **Mono Table Cells**  | `13px` (`0.8125rem`)| `400` / `500`   | `18px` | `0` | IPs, Ports, Latency, Confidence |

---

## 4. UI Components & Micro-Interactions

### 4.1. Traffic Status Badge
- **Normal Status**:
  - Background: `rgba(16, 185, 129, 0.15)`
  - Border: `1px solid rgba(16, 185, 129, 0.4)`
  - Text: `#34D399`
  - Indicator: Steady soft emerald pulse (`animation: pulse 2s infinite`).
- **Under Attack Status**:
  - Background: `rgba(239, 68, 68, 0.2)`
  - Border: `1px solid rgba(239, 68, 68, 0.6)`
  - Text: `#F87171`
  - Indicator: Rapid warning flash (`animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite`).

### 4.2. Glassmorphic Surface Styling
```css
.soc-card {
  background: rgba(17, 24, 39, 0.7);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.soc-card:hover {
  border-color: rgba(59, 130, 246, 0.25);
  box-shadow: 0 8px 25px -4px rgba(0, 0, 0, 0.6);
}
```

### 4.3. Data Visualizations & Charts
- **Palette for Attack Classification Chart**:
  - Normal Traffic: `#10B981` (Emerald)
  - DoS: `#EF4444` (Crimson)
  - Reconnaissance / PortScan: `#F59E0B` (Amber)
  - Exploits: `#8B5CF6` (Purple)
  - Fuzzers: `#06B6D4` (Cyan)
  - Unknown / Zero-Day Anomaly: `#EC4899` (Hot Pink)
- **Chart Background**: Transparent with faint grid lines (`#1E293B`, stroke-dasharray `3 3`).
