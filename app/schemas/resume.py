# app/schemas/resume.py
from pydantic import BaseModel, Field
from typing import List, Optional

class HeaderSection(BaseModel):
    full_name: str = Field(description="Candidate's full name")
    email: Optional[str] = Field(default=None, description="Primary email address")
    phone: Optional[str] = Field(default=None, description="Contact phone number")
    location: Optional[str] = Field(default=None, description="City, State, or Country")
    links: List[str] = Field(default_factory=list, description="LinkedIn, GitHub, Portfolio URLs")

class ExperienceItem(BaseModel):
    job_title: str
    company: str
    duration: Optional[str] = Field(default=None, description="e.g. Jan 2022 - Present")
    responsibilities: List[str] = Field(default_factory=list)

class ProjectItem(BaseModel):
    title: str
    description: str
    technologies: List[str] = Field(default_factory=list)

class EducationItem(BaseModel):
    degree: str
    institution: str
    year: Optional[str] = Field(default=None, description="Graduation year or date range")

class OrderedResume(BaseModel):
    """
    Fixed sequence:
    1. Header
    2. Profile
    3. Experience
    4. Projects
    5. Skills
    6. Education
    7. Certification
    """
    header: HeaderSection
    profile: Optional[str] = Field(default=None, description="Professional summary or objective statement")
    experience: List[ExperienceItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    certification: List[str] = Field(default_factory=list)