"""Pydantic models for due diligence reports.

This module defines the data structures used throughout the due diligence process.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class CompanyBasicInfo(BaseModel):
    """Basic company information."""
    name: str
    company_number: str
    status: str
    incorporation_date: str
    company_type: str
    registered_address: str
    jurisdiction: str = "United Kingdom"
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    business_description: Optional[str] = None


class CorporateStructure(BaseModel):
    """Corporate structure information."""
    parent_company: Optional[str] = None
    subsidiaries: List[str] = Field(default_factory=list)
    ultimate_parent: Optional[str] = None
    group_structure: Optional[str] = None
    share_capital: Optional[float] = None
    share_classes: Optional[List[str]] = None


class Officer(BaseModel):
    """Information about a company officer."""
    name: str
    role: str
    appointment_date: str
    nationality: Optional[str] = None
    date_of_birth: Optional[str] = None
    country_of_residence: Optional[str] = None
    other_directorships: Optional[List[str]] = None


class LeadershipInfo(BaseModel):
    """Company leadership and governance information."""
    directors: List[Officer] = Field(default_factory=list)
    company_secretary: Optional[Officer] = None
    key_management: Optional[List[Officer]] = None
    board_committees: Optional[List[str]] = None


class PSC(BaseModel):
    """Person with Significant Control information."""
    name: str
    nature_of_control: List[str]
    ownership_percentage: Optional[float] = None
    nationality: Optional[str] = None
    country_of_residence: Optional[str] = None


class OwnershipInfo(BaseModel):
    """Company ownership and control information."""
    persons_with_significant_control: List[PSC] = Field(default_factory=list)
    major_shareholders: Optional[List[dict]] = None
    beneficial_owners: Optional[List[dict]] = None


class FinancialMetrics(BaseModel):
    """Financial metrics for a specific period."""
    revenue: Optional[float] = None
    profit: Optional[float] = None
    assets: Optional[float] = None
    liabilities: Optional[float] = None
    cash_flow: Optional[float] = None
    financial_year_end: Optional[str] = None


class FinancialInfo(BaseModel):
    """Comprehensive financial information."""
    latest_financials: Optional[FinancialMetrics] = None
    historical_financials: Optional[List[FinancialMetrics]] = None
    key_ratios: Optional[dict] = None
    audit_status: Optional[str] = None
    accounting_policy: Optional[str] = None


class LegalInfo(BaseModel):
    """Legal and regulatory information."""
    charges: List[dict] = Field(default_factory=list)
    insolvency_history: Optional[List[dict]] = None
    regulatory_compliance: Optional[dict] = None
    pending_litigation: Optional[List[dict]] = None
    licenses_and_permits: Optional[List[str]] = None


class OperationalInfo(BaseModel):
    """Operational information."""
    number_of_employees: Optional[int] = None
    main_operating_locations: List[str] = Field(default_factory=list)
    key_products_services: List[str] = Field(default_factory=list)
    major_customers: Optional[List[str]] = None
    major_suppliers: Optional[List[str]] = None
    intellectual_property: Optional[List[str]] = None


class RiskFactor(BaseModel):
    """Individual risk factor."""
    category: str
    description: str
    severity: str
    mitigation: Optional[str] = None


class RiskAssessment(BaseModel):
    """Comprehensive risk assessment."""
    financial_risks: List[RiskFactor] = Field(default_factory=list)
    operational_risks: List[RiskFactor] = Field(default_factory=list)
    regulatory_risks: List[RiskFactor] = Field(default_factory=list)
    market_risks: List[RiskFactor] = Field(default_factory=list)
    reputational_risks: List[RiskFactor] = Field(default_factory=list)


class MarketInfo(BaseModel):
    """Market and industry information."""
    industry_classification: Optional[str] = None
    market_size: Optional[float] = None
    market_share: Optional[float] = None
    competitors: Optional[List[str]] = None
    industry_trends: Optional[List[str]] = None
    growth_prospects: Optional[str] = None


class ReportMetadata(BaseModel):
    """Report metadata and quality information."""
    version: str
    generated_by: str
    data_freshness: dict[str, datetime]
    confidence_scores: dict[str, float]
    limitations: List[str] = Field(default_factory=list)
    future_research_suggestions: List[str] = Field(default_factory=list)



