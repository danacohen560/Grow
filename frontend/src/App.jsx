import React, { useState, useEffect } from 'react'
import { jsPDF } from "jspdf"; 
import autoTable from "jspdf-autotable"; 
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import './App.css'

// Predefined career paths and their associated technical skills
const careerProfiles = {
  "Data Engineer": "Python, SQL, Apache Spark, ETL, Cloud Computing, Data Warehousing, Big Data",
  "Data Scientist": "Python, Machine Learning, Statistics, Data Analysis, SQL, Pandas, Deep Learning",
  "Full Stack Developer": "JavaScript, React, Node.js, HTML, CSS, MongoDB, Web Development",
  "Product Manager": "Product Management, Agile, Leadership, Market Research, Strategy, Data Analysis",
  "Cybersecurity Analyst": "Network Security, Python, Ethical Hacking, Risk Management, Linux, Cloud Security"
}

function App() {
  // Application state management
  const [skills, setSkills] = useState('')
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [hasSearched, setHasSearched] = useState(false)
  
  // UI and user preference states
  const [searchMode, setSearchMode] = useState('skills')
  const [platformFilter, setPlatformFilter] = useState('All')
  const [favorites, setFavorites] = useState([])
  const [viewMode, setViewMode] = useState('list'); 
  
  // State for dashboard statistics
  const [stats, setStats] = useState(null);

  const COLORS = ['#0ea5e9', '#6366f1', '#8b5cf6', '#ec4899', '#f43f5e'];

  // --- PDF Export Logic ---
  const exportToPDF = () => {
    try {
      const doc = new jsPDF();
      
      // Header Section
      doc.setFontSize(22);
      doc.setTextColor(99, 102, 241); 
      doc.text("EduSync - Your Learning Path", 14, 20);
      
      doc.setFontSize(10);
      doc.setTextColor(100);
      doc.text(`Target Skills: ${skills}`, 14, 30);
      doc.text(`Generated on: ${new Date().toLocaleString()}`, 14, 35);

      // Data Preparation
      const tableRows = recommendations.map((course, index) => [
        index + 1,
        course.platform,
        course.title,
        course.difficulty || 'Intermediate',
        course.instructor || 'Expert'
      ]);

      // Table Generation
      autoTable(doc, {
        startY: 45,
        head: [['#', 'Platform', 'Course Title', 'Level', 'Instructor']],
        body: tableRows,
        theme: 'striped',
        headStyles: { fill: [99, 102, 241], fontStyle: 'bold' },
        styles: { fontSize: 9, cellPadding: 3 },
      });

      doc.save(`EduSync_Learning_Path.pdf`);
    } catch (err) {
      console.error("PDF Export Error:", err);
      alert("Error generating PDF. Check the console.");
    }
  };

  // Data & Filtering Logic
  
  // Sort recommendations for the Roadmap view (Beginner -> Intermediate -> Advanced)
  const roadmapData = [...recommendations].sort((a, b) => a.difficulty_score - b.difficulty_score);

  const filteredRecommendations = recommendations.filter(course => 
    platformFilter === 'All' ? true : course.platform === platformFilter
  )

  // --- Side Effects ---
  useEffect(() => {
    fetch('https://grow-hkck.onrender.com/stats')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error("Error fetching stats:", err));
  }, []);

  useEffect(() => {
    const savedFavs = localStorage.getItem('courseFavorites')
    if (savedFavs) setFavorites(JSON.parse(savedFavs))
  }, [])

  useEffect(() => {
    localStorage.setItem('courseFavorites', JSON.stringify(favorites))
  }, [favorites])

  // --- Handlers ---
  const handleSearch = async (searchQuery = skills) => {
    if (!searchQuery) return;
    setSkills(searchQuery)
    setLoading(true)
    setError(null)
    setHasSearched(true)
    setPlatformFilter('All')
    
    try {
      const response = await fetch(`https://grow-hkck.onrender.com/recommend?skills=${encodeURIComponent(searchQuery)}`)
      if (!response.ok) throw new Error('Failed to fetch recommendations')
      const data = await response.json()
      setRecommendations(data.recommendations)
    } catch (err) {
      setError("Server connection failed")
    } finally {
      setLoading(false)
    }
  };

  const handleCareerSelect = (career) => {
    const suggestedSkills = careerProfiles[career]
    handleSearch(suggestedSkills)
  };

  const clearSearch = () => {
    setSkills('')
    setRecommendations([])
    setHasSearched(false)
  };

  const toggleFavorite = (course) => {
    const exists = favorites.find(fav => fav.url === course.url)
    if (exists) {
      setFavorites(favorites.filter(fav => fav.url !== course.url))
    } else {
      setFavorites([...favorites, course])
    }
  };

  return (
    <div className="app-container">
      <header>
        <div className="header-top">
          <h1 onClick={clearSearch} className="logo-title">GROW</h1>
          <div className="favorites-counter">
            ❤️ {favorites.length} Saved
          </div>
        </div>
        <p>Your personalized AI learning path generator</p>
      </header>

      {/* Mode Selection */}
      <div className="search-mode-tabs">
        <button className={`tab-btn ${searchMode === 'skills' ? 'active' : ''}`} onClick={() => setSearchMode('skills')}>Search Skills</button>
        <button className={`tab-btn ${searchMode === 'career' ? 'active' : ''}`} onClick={() => setSearchMode('career')}>Explore Career</button>
      </div>

      {searchMode === 'skills' ? (
        <div className="search-section">
          <input 
            type="text" 
            value={skills}
            onChange={(e) => setSkills(e.target.value)}
            placeholder="e.g. Python, SQL..."
            className="search-input"
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button onClick={() => handleSearch()} disabled={loading} className="search-button">
            {loading ? 'Thinking...' : 'Generate Path'}
          </button>
        </div>
      ) : (
        <div className="career-section">
          <div className="career-grid">
            {Object.keys(careerProfiles).map(career => (
              <button key={career} className="career-btn" onClick={() => handleCareerSelect(career)}>{career}</button>
            ))}
          </div>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}

      {/* --- DASHBOARD (Before Search) --- */}
      {!hasSearched && stats && (
        <div className="hero-content">
          <h2 className="hero-title">Course Market Trends</h2>
          <div className="dashboard-grid">
            <div className="chart-container">
              <h3>Popular Categories</h3>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={stats.category_data}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                  <XAxis dataKey="name" interval={0} angle={-25} textAnchor="end" height={60} tick={{fontSize: 10}} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                    {stats.category_data.map((entry, index) => <Cell key={index} fill={COLORS[index % COLORS.length]} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="chart-container">
              <h3>Platform Share</h3>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie data={stats.platform_data} innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                    {stats.platform_data.map((entry, index) => <Cell key={index} fill={COLORS[index % COLORS.length]} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="stats-banner">
             <div className="stat-item"><h3>{stats.total_courses}</h3><p>Courses Indexed</p></div>
             <div className="stat-item"><h3>AI</h3><p>Powered Matching</p></div>
          </div>
        </div>
      )}

      {/* --- RESULTS & ROADMAP (After Search) --- */}
      {hasSearched && (
        <div className="results-section">
          <div className="results-header">
            <h2>Your Custom Learning Path</h2>
            <div className="action-buttons">
              <div className="view-toggle">
                <button className={viewMode === 'list' ? 'active' : ''} onClick={() => setViewMode('list')}>List View</button>
                <button className={viewMode === 'roadmap' ? 'active' : ''} onClick={() => setViewMode('roadmap')}>Roadmap View</button>
              </div>
              <button className="export-btn" onClick={exportToPDF}>📥 PDF</button>
              <select value={platformFilter} onChange={(e) => setPlatformFilter(e.target.value)} className="platform-select">
                <option value="All">All Platforms</option>
                <option value="Coursera">Coursera</option>
                <option value="Udemy">Udemy</option>
              </select>
              <button className="clear-btn" onClick={clearSearch}>Clear</button>
            </div>
          </div>
          
          <div className={viewMode === 'list' ? 'cards-container' : 'roadmap-container'}>
            {(viewMode === 'list' ? filteredRecommendations : roadmapData).map((course, index) => {
                const isSaved = favorites.some(fav => fav.url === course.url);
                const isFirstOfLevel = viewMode === 'roadmap' && (index === 0 || roadmapData[index - 1].difficulty !== course.difficulty);
                
                return (
                  <React.Fragment key={index}>
                    {isFirstOfLevel && (
                      <div className="phase-divider">
                        <span>{course.difficulty} Phase</span>
                      </div>
                    )}
                    <div className={`course-card ${viewMode === 'roadmap' ? 'roadmap-step' : ''}`}>
                      {viewMode === 'roadmap' && <div className="step-number">{index + 1}</div>}
                      <div className="card-header">
                        <div>
                          <span className={`platform-badge ${course.platform.toLowerCase()}`}>{course.platform}</span>
                          <span className="difficulty-badge">{course.difficulty}</span>
                        </div>
                        <button className={`fav-btn ${isSaved ? 'saved' : ''}`} onClick={() => toggleFavorite(course)}>
                          {isSaved ? '❤️' : '🤍'}
                        </button>
                      </div>
                      <h3>{course.title}</h3>
                      <p className="instructor">by {course.instructor || 'Industry Experts'}</p>
                      <p>Match Score: <span className="score-tag">{(course.score * 100).toFixed(1)}%</span></p>
                      <a href={course.url} target="_blank" rel="noopener noreferrer" className="course-link">Explore Course ➔</a>
                    </div>
                  </React.Fragment>
                )
            })}
          </div>
        </div>
      )}
    </div>
  )
}

export default App