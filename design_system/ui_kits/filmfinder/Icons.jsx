// Icons — Lucide-style inline SVG components
const Icon = ({ d, size = 20, ...rest }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" className="ic" {...rest}>
    {d}
  </svg>
);

const Icons = {
  Search: (p) => <Icon {...p} d={<><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></>}/>,
  Bell: (p) => <Icon {...p} d={<><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></>}/>,
  BellOff: (p) => <Icon {...p} d={<><path d="M8.7 3A6 6 0 0 1 18 8c0 3 .7 5 1.5 6.5M6 8c0 7-3 9-3 9h15M10.3 21a1.94 1.94 0 0 0 3.4 0M2 2l20 20"/></>}/>,
  Heart: (p) => <Icon {...p} d={<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 1.51 4.04 3 5.5l7 7Z"/>}/>,
  HeartFill: (p) => <Icon {...p} d={<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 1.51 4.04 3 5.5l7 7Z" fill="currentColor"/>}/>,
  Calendar: (p) => <Icon {...p} d={<><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></>}/>,
  Clock: (p) => <Icon {...p} d={<><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></>}/>,
  Tv: (p) => <Icon {...p} d={<><rect x="2" y="7" width="20" height="15" rx="2"/><path d="m17 2-5 5-5-5"/></>}/>,
  Filter: (p) => <Icon {...p} d={<path d="M3 6h18M7 12h10M10 18h4"/>}/>,
  X: (p) => <Icon {...p} d={<path d="M18 6 6 18M6 6l12 12"/>}/>,
  Check: (p) => <Icon {...p} d={<path d="m5 12 4 4L19 7"/>}/>,
  Mail: (p) => <Icon {...p} d={<><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></>}/>,
  Trash: (p) => <Icon {...p} d={<><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/></>}/>,
  ArrowRight: (p) => <Icon {...p} d={<path d="M5 12h14M13 5l7 7-7 7"/>}/>,
  ChevronDown: (p) => <Icon {...p} d={<path d="m6 9 6 6 6-6"/>}/>,
};

window.Icons = Icons;
