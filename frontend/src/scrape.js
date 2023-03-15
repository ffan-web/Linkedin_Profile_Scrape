import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';

function Scraper() {
    const [targetUser, setTargetUser] = useState('');
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);


    const handleSubmit = async () => {
      const response = await fetch(`http://localhost:8080/scrape-profiles/${targetUser}`);
      console.log(response)
      const data = await response.json();
      console.log(data)
      setResponse(data);
      setLoading(false);
    }
    return (

        <div className="container my-5">
        <div className="row justify-content-center">
            <div className="col-md-8">
            <h1 className="text-center mb-5" style={{ color: '#0077B5' }}>LinkedIn Profile Scraper</h1>
            <form>
                <div className="mb-3">
                <label htmlFor="targetUser" className="form-label">Enter a LinkedIn Account Name</label>
                <div className="input-group">
                    <input type="text" className="form-control" id="targetUser" value={targetUser} onChange={(e) => setTargetUser(e.target.value)} placeholder="e.g. john-doe"/>
                    <button type="button" className="btn btn-primary" onClick={handleSubmit}>Submit</button>
                </div>
                </div>
            </form>
            </div>
        </div>
        {response && <Response data={response} />}
        </div>
      
    );
  }
  
  function Education({ educations }) {
    return (
        <div className="row mt-5">
        <div className="col">
          <h2>Education</h2>
          <hr/>
          <ul>
            {educations.map((item, index) => (
              <li key ={index}>
                <h5>{item.School}</h5>
                <p className="mb-0">{item.Degree}</p>
                <p className="mb-0">{item.DateRange}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  }

  function Experience({ experiences }) {
    return (
        <div className="row mt-5">
        <div className="col">
          <h2>Experience</h2>
          <hr/>
          <ul>
            {experiences.map((item, index) => (
              <li key ={index}>
                <h5>{item.Company}</h5>
                <p className="mb-0">{item.Title}</p>
                <p className="mb-0">{item.DateRange}</p>
                <p>{item.Location}</p>
                <p>{item.JobContent}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  }

  function Recommendation({ recommendations }) {
    return (
        <div className="row mt-5">
        <div className="col">
          <h2>Recommendations</h2>
          <hr/>
          <ul>
            {recommendations.map((item, index) => (
              <li key ={index}>
                <h5>{item.Name}</h5>
                <p className="mb-0">{item.Relation}</p>
                <p className="mb-0">{item.Date}</p>
                <p className="mb-0"><a href={item.Link}>{item.Link}</a></p>
                <p>{item.Content}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    );
  }

  function Response({ data }) {
    return (
      <div className="container">
        <div className="card mt-4">
            <div className="card-body">
                <h2 className="card-title">{data.Name}</h2>
                <p className="card-subtitle mb-2 text-muted">{data.Title}</p>
                <p className="card-subtitle mb-2 text-muted">{data.Location}</p>
                <p className="card-subtitle mb-2 text-muted">{data.About}</p>
                <Education educations = { data.Education } />
                <Experience experiences = { data.Experience } />
                <Recommendation recommendations = { data.Recommendation } />
            </div>
        </div>
      </div>
    );
  }
  
  export default Scraper;