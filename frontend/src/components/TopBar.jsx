export default function TopBar({ modo }) {
  return (
    <div className="topbar">
      <svg className="bolt" viewBox="0 0 24 24" fill="#ffd44d" aria-hidden="true">
        <path d="M13 2 4 14h6l-1 8 9-12h-6z" />
      </svg>
      <div className="logo">EnergiAI</div>
      <div className="spacer" />
      <span className="mode">{modo}</span>
      <div className="avatar">72</div>
    </div>
  )
}
