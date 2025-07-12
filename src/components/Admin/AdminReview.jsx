import React, { useState, useEffect } from 'react';
import Select from 'react-select';
import './AdminReview.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';



const AdminReview = () => {

  const [profilesData, setProfilesData] = useState({});
  const [loading, setLoading] = useState(true);
  const [reviewers, setReviewers] = useState([]);
  const [hrReviewers, setHrReviewers] = useState([]);
  const [managers, setManagers] = useState([]);
// Change - 1  
  const [verticals, setVerticals] = useState([]); 
  const [divisions, setDivisions] = useState([]);
  const [subdivisions, setSubdivisions] = useState([]);
// Change - 1 End
// useEffect(() => {
//   const fetchProfiles = async () => {
//     try {
//       // const response = await fetch('http://18.224.60.64:5000/api/admin-review');
//       const response = await fetch('http://18.224.60.64:5000/api/all-job-profiles');
//       const data = await response.json();
//       setProfilesData(data);
//       setLoading(false);

// // Change - 2 Extracting unique verticals, divisions, and subdivisions
//       const uniqueVerticals = new Set();
//       const uniqueDivisions = new Set();
//       const uniqueSubdivisions = new Set();

//         Object.values(data).forEach(profile => {
//           if (profile.vertical) uniqueVerticals.add(profile.vertical);
//           if (profile.division) uniqueDivisions.add(profile.division);
//           if (profile.subdivision) uniqueSubdivisions.add(profile.subdivision);
//         });

//         setVerticals([...uniqueVerticals]);
//         setDivisions([...uniqueDivisions]);
//         setSubdivisions([...uniqueSubdivisions]);

//     } catch (error) {
//       console.error("Error fetching profiles:", error);
//       setLoading(false);
//     }
//   };

//   fetchProfiles();
// }, []);

// BEFORE useEffect
const fetchProfiles = async () => {
  try {
    const response = await fetch('http://18.224.60.64:5000/api/all-job-profiles');
    const data = await response.json();
    setProfilesData(data);
    setLoading(false);

    const uniqueVerticals = new Set();
    const uniqueDivisions = new Set();
    const uniqueSubdivisions = new Set();

    Object.values(data).forEach(profile => {
      if (profile.vertical) uniqueVerticals.add(profile.vertical);
      if (profile.division) uniqueDivisions.add(profile.division);
      if (profile.subdivision) uniqueSubdivisions.add(profile.subdivision);
    });

    setVerticals([...uniqueVerticals]);
    setDivisions([...uniqueDivisions]);
    setSubdivisions([...uniqueSubdivisions]);

  } catch (error) {
    console.error("Error fetching profiles:", error);
    setLoading(false);
  }
};

// useEffect(() => {
//   fetchProfiles();
// }, [selectedProfile]);


useEffect(() => {
  const fetchReviewers = async () => {
    try {
      const response = await fetch('http://18.224.60.64:5000/api/reviewers-list');
      const data = await response.json();
      setReviewers(data.primaryReviewers || []);
      setHrReviewers(data.hrReviewers || []);
      setManagers(data.managers || []);
    } catch (error) {
      console.error('Error fetching reviewers:', error);
    }
  };

  fetchReviewers();
}, []);



  const [selectedProfile, setSelectedProfile] = useState('');

  useEffect(() => {
    fetchProfiles();
  }, []);

  const [mainEditable, setMainEditable] = useState(false);
  const [sectionEditable, setSectionEditable] = useState({
    purpose: false,
    responsibilities: false,
    manager: false,
    travel: false,
    physical: false,
    workconditions: false,
    minqualifications: false,
    preferredqualifications: false,
    mineducation: false,
    preferrededucation: false,
    minexperience: false,
    certifications: false,
    competencies: false
  });

  const [formState, setFormState] = useState({
    primaryReviewer: '',
    hrReviewer: '',
    hiringManager: '',
    vertical: '',
    division: '',
    subdivision: '',
    purpose: '',
    responsibilities: '',
    manager: '',
    travel: '',
    physical: '',
    workconditions: '',
    minqualifications: '',
    preferredqualifications: '',
    mineducation: '',
    preferrededucation: '',
    minexperience: '',
    certifications: '',
    competencies: ''
  });

  const [editBuffer, setEditBuffer] = useState({
    primaryReviewer: '',
    hrReviewer: '',
    hiringManager: '',
    vertical: '',
    division: '',
    subdivision: '',
    purpose: '',
    responsibilities: '',
    manager: '',
    travel: '',
    physical: '',
    workconditions: '',
    minqualifications: '',
    preferredqualifications: '',
    mineducation: '',
    preferrededucation: '',
    minexperience: '',
    certifications: '',
    competencies: ''
  });


const addPrimaryReviewer = async (name) => {
  setReviewers(prev => [...prev, name]);
  setEditBuffer(prev => ({ ...prev, primaryReviewer: name }));

  try {
    await fetch('http://18.224.60.64:5000/api/admin-reviewers/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, type: 'primary' })
    });
    console.log('Primary reviewer saved to backend');
  } catch (error) {
    console.error('Failed to save primary reviewer:', error);
  }
};

const addHRReviewer = async (name) => {
  setHrReviewers(prev => [...prev, name]);
  setEditBuffer(prev => ({ ...prev, hrReviewer: name }));

  try {
    await fetch('http://18.224.60.64:5000/api/admin-reviewers/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, type: 'hr' })
    });
    console.log('HR reviewer saved to backend');
  } catch (error) {
    console.error('Failed to save HR reviewer:', error);
  }
};

const addHiringManager = async (name) => {
  setManagers(prev => [...prev, name]);
  setEditBuffer(prev => ({ ...prev, hiringManager: name }));

  try {
    await fetch('http://18.224.60.64:5000/api/admin-reviewers/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, type: 'manager' })
    });
    console.log('Hiring manager saved to backend');
  } catch (error) {
    console.error('Failed to save hiring manager:', error);
  }
};

  

  const handleProfileSelect = (profile) => {
    const profileData = profilesData[profile];

    if (!profileData) {
      console.error("Profile data not found for selected profile:", profile);
      return;
    }


    const newState = {
      primaryReviewer: profileData.primaryReviewer,
      hrReviewer: profileData.hrReviewer,
      hiringManager: profileData.hiringManager,
      vertical: profileData.vertical,
      division: profileData.division,
      subdivision: profileData.subdivision,
      purpose: profileData.description.purpose,
      responsibilities: profileData.description.responsibilities,
      manager: profileData.description.manager,
      travel: profileData.description.travel,
      physical: profileData.description.physical,
      workconditions: profileData.description.workconditions,
      minqualifications: profileData.description.minqualifications,
      preferredqualifications: profileData.description.preferredqualifications,
      mineducation: profileData.description.mineducation,
      preferrededucation: profileData.description.preferrededucation,
      minexperience: profileData.description.minexperience,
      certifications: profileData.description.certifications,
      competencies: profileData.description.competencies
    };

  

    setFormState(newState);
    
    setEditBuffer(newState);

    setSelectedProfile(profile);

    setMainEditable(false);
    
    
    
    setSectionEditable({ 
      purpose: false, 
      responsibilities: false, 
      manager: false, 
      travel: false, 
      physical: false, 
      workconditions: false, 
      minqualifications: false, 
      preferredqualifications: false, 
      mineducation: false, 
      preferrededucation: false, 
      minexperience: false, 
      certifications: false, 
      competencies: false 
    });
  };

  const toggleSectionEdit = (section) => {
    setSectionEditable(prev => {
      const isNowActive = !prev[section];

      if (!isNowActive) {
        setEditBuffer(prevEdit => ({
          ...prevEdit,
          [section]: formState[section]
        }));
      }

      return { ...prev, [section]: isNowActive };
    });
  };

  const handleSave = async () => {
    try {
      const response = await fetch('http://18.224.60.64:5000/api/admin-review/update', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          profile: selectedProfile,
          updatedData: editBuffer
        }),
      });
  
      if (response.ok) {
        setFormState(editBuffer);
        setMainEditable(false);
  
        const resetSections = {};
        Object.keys(sectionEditable).forEach(key => {
          resetSections[key] = false;
        });
        setSectionEditable(resetSections);

        await fetchProfiles();  
  
        // alert("Changes saved successfully!");
        toast.success("Changes saved successfully!");

      } else {
        // alert("Failed to save changes.");
        toast.error("Failed to save changes.");
      }
    } catch (error) {
      console.error("Error saving changes:", error);
      // alert("Error saving changes.");
        toast.error("Failed to save changes.");

    }
  };
  


  if (loading) {
    return <div>Loading profiles...</div>;
  }
  

  return (


<div className="admin-page-wrapper">
  {/* Header */}
  <header className="admin-header">
    <img src='./Header.jpg' alt="Header" className="header-photo" />
  </header>



<div className="admin-review-container">
      <h2 className="admin-heading">Admin Review</h2>

      <div className="profile-edit-row">
  {/* <div className="profile-dropdown">
    <label>Job Profile</label>
    <select
      className="dropdown"
      value={selectedProfile}
      onChange={e => handleProfileSelect(e.target.value)}
    >
      <option value="">Select Profile</option>
      {/* {Object.keys(profilesData).map(profile => (
        <option key={profile} value={profile}>{profile}</option>
      ))} */} {/*
      {profilesData ? (
        Object.keys(profilesData).map(profile => (
          <option key={profile} value={profile}>{profile}</option>
        ))
      ) : (
        <option>Loading profiles...</option>
      )}
    </select>
  </div> */}

<div className="profile-dropdown">
  <label>Job Profile</label>
  <Select
    options={Object.keys(profilesData).map(profile => ({
      value: profile,
      label: profile
    }))}
    value={selectedProfile ? { label: selectedProfile, value: selectedProfile } : null}
    onChange={(option) => handleProfileSelect(option.value)}
    placeholder="Select Profile"
    isSearchable
    className="react-select-container"
    classNamePrefix="react-select"
  />
</div>

  <div className="edit-button-container">
    {selectedProfile && (
      <button
        className="edit-button"
        onClick={() => {
          if (mainEditable) {
            const resetSections = {};
            Object.keys(sectionEditable).forEach(key => {
              resetSections[key] = false;
            });
            setSectionEditable(resetSections);
            setEditBuffer(formState);
          } else {
            const activateSections = {};
            Object.keys(sectionEditable).forEach(key => {
              activateSections[key] = true;
            });
            setSectionEditable(activateSections);
          }
        
          setMainEditable(!mainEditable);
        }}
        
      >
        {mainEditable ? 'Cancel Edit' : 'Edit'}
      </button>
    )}
  </div>
</div>


      {selectedProfile && (
        <>
          <div className="reviewer-row">
  <div className="reviewer-dropdown">
    <label>Primary Reviewer</label>
    <div className="dropdown-button-group">
      <select
        className="dropdown"
        value={mainEditable ? editBuffer.primaryReviewer : formState.primaryReviewer}
        onChange={e => setEditBuffer(prev => ({ ...prev, primaryReviewer: e.target.value }))}
        disabled={!mainEditable}
      >
        {reviewers.map(rev => (
          <option key={rev} value={rev}>{rev}</option>
        ))}
      </select>
      {mainEditable ? (
        <button
          className="add-new-button"
          onClick={() => {
            const name = prompt("Enter new Primary Reviewer name:");
            if (name) addPrimaryReviewer(name);
          }}
        >
          ➕ Add
        </button>
      ) :(
        <div className="dropdown-button-placeholder"></div>
      )}
    </div>
  </div>

  <div className="reviewer-dropdown">
    <label>HR Reviewer</label>
    <div className="dropdown-button-group">
      <select
        className="dropdown"
        value={mainEditable ? editBuffer.hrReviewer : formState.hrReviewer}
        onChange={e => setEditBuffer(prev => ({ ...prev, hrReviewer: e.target.value }))}
        disabled={!mainEditable}
      >
        {hrReviewers.map(hr => (
          <option key={hr} value={hr}>{hr}</option>
        ))}
      </select>
      {mainEditable ? (
        <button
          className="add-new-button"
          onClick={() => {
            const name = prompt("Enter new HR Reviewer name:");
            if (name) addHRReviewer(name);
          }}
        >
          ➕ Add
        </button>
        ) :(
          <div className="dropdown-button-placeholder"></div>
      )}
    </div>
  </div>

  <div className="reviewer-dropdown">
    <label>Hiring Manager</label>
    <div className="dropdown-button-group">
      <select
        className="dropdown"
        value={mainEditable ? editBuffer.hiringManager : formState.hiringManager}
        onChange={e => setEditBuffer(prev => ({ ...prev, hiringManager: e.target.value }))}
        disabled={!mainEditable}
      >
        {managers.map(mgr => (
          <option key={mgr} value={mgr}>{mgr}</option>
        ))}
      </select>
      {mainEditable ? (
        <button
          className="add-new-button"
          onClick={() => {
            const name = prompt("Enter new hiring manager name:");
            if (name) addHiringManager(name);
          }}
        >
          ➕ Add
        </button>

) :(
  <div className="dropdown-button-placeholder"></div>
      )}
    </div>
  </div>
</div>



          <div className="readonly-combined-box">
{/* Change - 3 */}


<div>
        <strong>Vertical:</strong>
        {mainEditable ? (
          <select
            className="inline-input"
            value={editBuffer.vertical}
            onChange={(e) => setEditBuffer(prev => ({ ...prev, vertical: e.target.value }))}
          >
            {verticals.map(v => <option key={v} value={v}>{v}</option>)}
          </select>
        ) : (
          <span> {formState.vertical}</span>
        )}
      </div>

{/* Change - 3 End */}



{/* Change - 4 */}

<div>
        <strong>Division:</strong>
        {mainEditable ? (
          <select
            className="inline-input"
            value={editBuffer.division}
            onChange={(e) => setEditBuffer(prev => ({ ...prev, division: e.target.value }))}
          >
            {divisions.map(d => <option key={d} value={d}>{d}</option>)}
          </select>
        ) : (
          <span> {formState.division}</span>
        )}
      </div>

{/* Change - 4 End */}


{/* Change - 5 */}


<div>
        <strong>Sub Division:</strong>
        {mainEditable ? (
          <select
            className="inline-input"
            value={editBuffer.subdivision}
            onChange={(e) => setEditBuffer(prev => ({ ...prev, subdivision: e.target.value }))}
          >
            {subdivisions.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        ) : (
          <span> {formState.subdivision}</span>
        )}
      </div>

{/* Change - 5 End */}



</div>


          <div className="job-description-header">
            <h3>Job Description</h3>
            
          </div>

          {["purpose",
          "responsibilities",
          "manager",
          "travel",
          "physical",
          "workconditions",
          "minqualifications",
          "preferredqualifications",
          "mineducation",
          "preferrededucation",
          "minexperience",
          "certifications",
          "competencies"].map((key) => (
            <div key={key} className="description-section">
              <div className="section-header">
                <h4>{{
                  purpose: "Position Purpose",
                  responsibilities: "Key Responsibilities",
                  manager: "Direct Manager/Direct Reports",
                  travel: "Travel Requirements",
                  physical: "Physical Requirements",
                  workconditions: "Working Conditions",
                  minqualifications: "Minimum Qualifications",
                  preferredqualifications: "Preferred Qualifications",
                  mineducation: "Minimum Education",
                  preferrededucation: "Preferred Education",
                  minexperience: "Minimum Experience",
                  certifications: "Certifications",
                  competencies: "Competencies"
                }[key]}</h4>

                {mainEditable && (
                  <button
                    className="section-edit-button"
                    onClick={() => toggleSectionEdit(key)}
                  >
                    {sectionEditable[key] ? 'Cancel' : 'Edit'}
                  </button>
                )}
              </div>



              {!sectionEditable[key] ? (
                // <p>{mainEditable ? editBuffer[key] : formState[key]}</p>
                <p>
  {formState[key]?.split('\n').map((line, index) => (
    <React.Fragment key={index}>
      {line}
      <br />
    </React.Fragment>
  ))}
</p>
              ) : (
                <>
                  <textarea
                    value={editBuffer[key]}
                    onChange={(e) => setEditBuffer(prev => ({ ...prev, [key]: e.target.value }))}
                    rows={4}
                    className="editable-textarea"
                  />
                </>
              )}
            </div>
          ))}

          {mainEditable && (
            <div style={{ marginTop: '20px' }}>
              <button className="save-button" onClick={handleSave}>
                Save Changes
              </button>
            </div>
          )}
        </>
      )}
    </div>






      <ToastContainer position="top-center" autoClose={3000} hideProgressBar />




    <footer className="admin-footer">
    <img src="./orgnest_logo.png" alt="Company Logo" className="footer-logo" />
    <p>© 2025 OrgNest. All rights reserved. <a href="/privacy">Privacy Policy</a></p>
  </footer>
</div>





  );
};

export default AdminReview;
