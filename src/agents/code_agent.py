#!/usr/bin/env python3
"""
Code Agent - Generates and Updates Python Code from Story Specifications

This agent reads story specs and generates or updates Python code in the MyBank repository,
focusing on banking domain implementations with proper architecture patterns.
"""
import sys
import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

class CodeAgent:
    """
    Code Agent for generating Python code from story specifications.
    
    Actions:
    - generate_code_snippet: Create code from story requirements
    - commit_changes: Automated Git operations
    """
    
    def __init__(self):
        """Initialize the code agent."""
        self.agent_id = "code-agent"
        self.version = "1.0"
        self.mybank_root = project_root / "src" / "MyBank"
        self.specs_root = project_root / "specs"
        
        # Ensure MyBank directory structure exists
        self._initialize_mybank_structure()
    
    def _initialize_mybank_structure(self):
        """Initialize the MyBank directory structure."""
        mybank_dirs = [
            "accounts",
            "loans", 
            "credit_cards",
            "payments",
            "investments",
            "fraud_detection",
            "compliance",
            "shared",
            "api",
            "tests"
        ]
        
        for dir_name in mybank_dirs:
            dir_path = self.mybank_root / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py if it doesn't exist
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                init_file.write_text(f'"""MyBank {dir_name.title()} Module"""\n')
    
    def generate_code_from_specs(self, agent_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for generating code from specifications.
        
        Args:
            agent_params: Parameters from orchestrator including prompt, specs, etc.
            
        Returns:
            Code generation result with created files and commit info
        """
        prompt = agent_params.get("prompt", "")
        banking_context = agent_params.get("banking_context", {})
        entities = agent_params.get("entities", {})
        
        print(f"🔧 Code Agent Processing: {prompt}")
        
        result = {
            "agent_id": self.agent_id,
            "processing_timestamp": datetime.now().isoformat(),
            "input_prompt": prompt,
            "banking_context": banking_context,
            "status": "processing",
            "generated_files": [],
            "updated_files": [],
            "commit_info": None,
            "errors": []
        }
        
        try:
            # Analyze prompt to determine code generation approach
            code_analysis = self._analyze_code_requirements(prompt, banking_context, entities)
            
            # Generate code based on analysis
            if code_analysis["type"] == "banking_feature":
                generation_result = self._generate_banking_feature_code(code_analysis)
            elif code_analysis["type"] == "fraud_detection":
                generation_result = self._generate_fraud_detection_code(code_analysis)
            elif code_analysis["type"] == "compliance":
                generation_result = self._generate_compliance_code(code_analysis)
            elif code_analysis["type"] == "api":
                generation_result = self._generate_api_code(code_analysis)
            else:
                generation_result = self._generate_generic_code(code_analysis)
            
            result.update(generation_result)
            
            # Auto-commit if successful
            if generation_result.get("generated_files") or generation_result.get("updated_files"):
                commit_result = self.commit_changes(result)
                result["commit_info"] = commit_result
            
            result["status"] = "completed"
            
        except Exception as e:
            result["status"] = "error"
            result["errors"].append(str(e))
            print(f"❌ Error in code generation: {e}")
        
        return result
    
    def _analyze_code_requirements(self, prompt: str, banking_context: Dict[str, Any], entities: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze prompt to determine code generation requirements."""
        prompt_lower = prompt.lower()
        
        analysis = {
            "type": "generic",
            "domain": "general",
            "components": [],
            "patterns": [],
            "technologies": entities.get("technologies", []),
            "banking_products": banking_context.get("product_types", []),
            "compliance_areas": banking_context.get("compliance_areas", [])
        }
        
        # Determine primary type
        if any(keyword in prompt_lower for keyword in ["fraud", "detection", "monitoring", "alert"]):
            analysis["type"] = "fraud_detection"
            analysis["domain"] = "fraud_detection"
        elif any(keyword in prompt_lower for keyword in ["compliance", "kyc", "aml", "pci", "audit"]):
            analysis["type"] = "compliance"
            analysis["domain"] = "compliance"
        elif any(keyword in prompt_lower for keyword in ["api", "endpoint", "service", "microservice"]):
            analysis["type"] = "api"
            analysis["domain"] = "api"
        elif banking_context.get("is_banking"):
            analysis["type"] = "banking_feature"
            analysis["domain"] = banking_context.get("primary_product", "general")
        
        # Identify components to generate
        if "class" in prompt_lower or "model" in prompt_lower:
            analysis["components"].append("model")
        if "api" in prompt_lower or "endpoint" in prompt_lower:
            analysis["components"].append("api")
        if "service" in prompt_lower:
            analysis["components"].append("service")
        if "test" in prompt_lower:
            analysis["components"].append("test")
        if "database" in prompt_lower or "db" in prompt_lower:
            analysis["components"].append("database")
        
        # Default components if none specified
        if not analysis["components"]:
            analysis["components"] = ["model", "service"]
        
        # Identify design patterns
        if "factory" in prompt_lower:
            analysis["patterns"].append("factory")
        if "observer" in prompt_lower or "event" in prompt_lower:
            analysis["patterns"].append("observer")
        if "strategy" in prompt_lower:
            analysis["patterns"].append("strategy")
        
        return analysis
    
    def _generate_banking_feature_code(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code for banking domain features."""
        print("🏦 Generating Banking Feature Code...")
        
        domain = analysis["domain"]
        components = analysis["components"]
        generated_files = []
        
        # Generate domain-specific module
        if "model" in components:
            model_file = self._generate_banking_model(domain, analysis)
            if model_file:
                generated_files.append(model_file)
        
        if "service" in components:
            service_file = self._generate_banking_service(domain, analysis)
            if service_file:
                generated_files.append(service_file)
        
        if "api" in components:
            api_file = self._generate_banking_api(domain, analysis)
            if api_file:
                generated_files.append(api_file)
        
        return {
            "generation_type": "banking_feature",
            "domain": domain,
            "generated_files": generated_files,
            "patterns_used": analysis.get("patterns", [])
        }
    
    def _generate_fraud_detection_code(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fraud detection specific code."""
        print("🔍 Generating Fraud Detection Code...")
        
        generated_files = []
        
        # Fraud detection model
        fraud_model = self._create_fraud_detection_model()
        if fraud_model:
            generated_files.append(fraud_model)
        
        # Transaction monitor
        transaction_monitor = self._create_transaction_monitor()
        if transaction_monitor:
            generated_files.append(transaction_monitor)
        
        # Alert system
        alert_system = self._create_alert_system()
        if alert_system:
            generated_files.append(alert_system)
        
        return {
            "generation_type": "fraud_detection",
            "generated_files": generated_files,
            "ml_components": True,
            "real_time_processing": True
        }
    
    def _generate_compliance_code(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate compliance-specific code."""
        print("📋 Generating Compliance Code...")
        
        compliance_areas = analysis.get("compliance_areas", [])
        generated_files = []
        
        # Compliance validator
        validator_file = self._create_compliance_validator(compliance_areas)
        if validator_file:
            generated_files.append(validator_file)
        
        # Audit logger
        audit_logger = self._create_audit_logger()
        if audit_logger:
            generated_files.append(audit_logger)
        
        # Compliance reporter
        reporter_file = self._create_compliance_reporter(compliance_areas)
        if reporter_file:
            generated_files.append(reporter_file)
        
        return {
            "generation_type": "compliance",
            "compliance_areas": compliance_areas,
            "generated_files": generated_files,
            "audit_capabilities": True
        }
    
    def _generate_api_code(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate API-specific code."""
        print("🌐 Generating API Code...")
        
        generated_files = []
        
        # API endpoints
        api_file = self._create_api_endpoints(analysis)
        if api_file:
            generated_files.append(api_file)
        
        # API models
        models_file = self._create_api_models(analysis)
        if models_file:
            generated_files.append(models_file)
        
        return {
            "generation_type": "api",
            "generated_files": generated_files,
            "rest_api": True
        }
    
    def _generate_generic_code(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate generic code based on analysis."""
        print("⚙️ Generating Generic Code...")
        
        generated_files = []
        
        # Basic module structure
        module_file = self._create_generic_module(analysis)
        if module_file:
            generated_files.append(module_file)
        
        return {
            "generation_type": "generic",
            "generated_files": generated_files
        }
    
    def _generate_banking_model(self, domain: str, analysis: Dict[str, Any]) -> Optional[str]:
        """Generate banking domain model."""
        try:
            model_name = f"{domain.title()}Model"
            filename = f"{domain}_model.py"
            filepath = self.mybank_root / domain / filename
            
            # Ensure directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            content = f'''"""
{domain.title()} Domain Model for MyBank

Generated by Code Agent on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from decimal import Decimal
from datetime import datetime
import uuid


@dataclass
class {model_name}:
    """
    {domain.title()} domain model with banking-specific attributes.
    """
    id: str = None
    customer_id: str = None
    created_at: datetime = None
    updated_at: datetime = None
    status: str = "active"
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values after creation."""
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.metadata is None:
            self.metadata = {{}}
    
    def update_status(self, new_status: str) -> None:
        """Update model status with timestamp."""
        self.status = new_status
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary representation."""
        return {{
            "id": self.id,
            "customer_id": self.customer_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "status": self.status,
            "metadata": self.metadata
        }}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "{model_name}":
        """Create model instance from dictionary."""
        return cls(
            id=data.get("id"),
            customer_id=data.get("customer_id"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None,
            status=data.get("status", "active"),
            metadata=data.get("metadata", {{}})
        )


class {model_name}Repository:
    """Repository pattern for {domain} data access."""
    
    def __init__(self):
        """Initialize repository."""
        self._data_store = {{}}  # In-memory store for demo
    
    def save(self, model: {model_name}) -> {model_name}:
        """Save model to data store."""
        model.updated_at = datetime.now()
        self._data_store[model.id] = model
        return model
    
    def find_by_id(self, model_id: str) -> Optional[{model_name}]:
        """Find model by ID."""
        return self._data_store.get(model_id)
    
    def find_by_customer_id(self, customer_id: str) -> List[{model_name}]:
        """Find all models for a customer."""
        return [
            model for model in self._data_store.values()
            if model.customer_id == customer_id
        ]
    
    def find_by_status(self, status: str) -> List[{model_name}]:
        """Find models by status."""
        return [
            model for model in self._data_store.values()
            if model.status == status
        ]
    
    def delete(self, model_id: str) -> bool:
        """Delete model by ID."""
        if model_id in self._data_store:
            del self._data_store[model_id]
            return True
        return False
'''
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Generated banking model: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error generating banking model: {e}")
            return None
    
    def _generate_banking_service(self, domain: str, analysis: Dict[str, Any]) -> Optional[str]:
        """Generate banking domain service."""
        try:
            service_name = f"{domain.title()}Service"
            filename = f"{domain}_service.py"
            filepath = self.mybank_root / domain / filename
            
            content = f'''"""
{domain.title()} Service for MyBank

Business logic and service layer for {domain} operations.
Generated by Code Agent on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

try:
    from .{domain}_model import {domain.title()}Model, {domain.title()}ModelRepository
except ImportError:
    # Fallback if model not available
    class {domain.title()}Model:
        pass
    class {domain.title()}ModelRepository:
        pass

logger = logging.getLogger(__name__)


class {service_name}:
    """
    Service class for {domain} business operations.
    """
    
    def __init__(self, repository: {domain.title()}ModelRepository = None):
        """Initialize service with repository."""
        self.repository = repository or {domain.title()}ModelRepository()
        self.logger = logger
    
    def create_{domain}(self, customer_id: str, **kwargs) -> {domain.title()}Model:
        """
        Create a new {domain} for a customer.
        
        Args:
            customer_id: Customer identifier
            **kwargs: Additional {domain} attributes
            
        Returns:
            Created {domain} model
        """
        try:
            # Create new model instance
            model = {domain.title()}Model(
                customer_id=customer_id,
                **kwargs
            )
            
            # Business validation
            self._validate_{domain}_creation(model)
            
            # Save to repository
            saved_model = self.repository.save(model)
            
            self.logger.info(f"Created {domain} {{saved_model.id}} for customer {{customer_id}}")
            return saved_model
            
        except Exception as e:
            self.logger.error(f"Error creating {domain} for customer {{customer_id}}: {{e}}")
            raise
    
    def get_{domain}(self, model_id: str) -> Optional[{domain.title()}Model]:
        """
        Get {domain} by ID.
        
        Args:
            model_id: {domain.title()} identifier
            
        Returns:
            {domain.title()} model or None if not found
        """
        return self.repository.find_by_id(model_id)
    
    def get_customer_{domain}s(self, customer_id: str) -> List[{domain.title()}Model]:
        """
        Get all {domain}s for a customer.
        
        Args:
            customer_id: Customer identifier
            
        Returns:
            List of {domain} models
        """
        return self.repository.find_by_customer_id(customer_id)
    
    def update_{domain}_status(self, model_id: str, new_status: str) -> Optional[{domain.title()}Model]:
        """
        Update {domain} status.
        
        Args:
            model_id: {domain.title()} identifier
            new_status: New status value
            
        Returns:
            Updated model or None if not found
        """
        model = self.repository.find_by_id(model_id)
        if model:
            model.update_status(new_status)
            updated_model = self.repository.save(model)
            self.logger.info(f"Updated {domain} {{model_id}} status to {{new_status}}")
            return updated_model
        return None
    
    def _validate_{domain}_creation(self, model: {domain.title()}Model) -> None:
        """
        Validate {domain} creation business rules.
        
        Args:
            model: {domain.title()} model to validate
            
        Raises:
            ValueError: If validation fails
        """
        if not model.customer_id:
            raise ValueError("Customer ID is required")
        
        # Add domain-specific validation rules here
        self.logger.debug(f"Validated {domain} model {{model.id}}")
    
    def process_{domain}_business_logic(self, model_id: str, **kwargs) -> Dict[str, Any]:
        """
        Execute domain-specific business logic.
        
        Args:
            model_id: {domain.title()} identifier
            **kwargs: Additional parameters for business logic
            
        Returns:
            Business operation result
        """
        model = self.repository.find_by_id(model_id)
        if not model:
            raise ValueError(f"{domain.title()} not found: {{model_id}}")
        
        # Implement domain-specific business logic
        result = {{
            "model_id": model_id,
            "operation": "business_logic_executed",
            "timestamp": datetime.now().isoformat(),
            "result": "success"
        }}
        
        self.logger.info(f"Executed business logic for {domain} {{model_id}}")
        return result
'''
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Generated banking service: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error generating banking service: {e}")
            return None
    
    def _create_fraud_detection_model(self) -> Optional[str]:
        """Create fraud detection model."""
        try:
            filepath = self.mybank_root / "fraud_detection" / "fraud_detector.py"
            
            content = '''"""
Fraud Detection Model for MyBank

Real-time fraud detection with machine learning capabilities.
Generated by Code Agent
"""
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
from decimal import Decimal
import json


@dataclass
class Transaction:
    """Transaction data model for fraud detection."""
    id: str
    customer_id: str
    amount: Decimal
    merchant: str
    location: str
    timestamp: datetime
    card_number_hash: str
    transaction_type: str
    metadata: Dict[str, Any] = None


@dataclass
class FraudScore:
    """Fraud risk score result."""
    transaction_id: str
    score: float  # 0.0 to 1.0 (higher = more suspicious)
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    factors: List[str]
    recommendation: str  # APPROVE, REVIEW, DECLINE, BLOCK_CARD


class FraudDetector:
    """
    Real-time fraud detection engine with ML capabilities.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize fraud detector with configuration."""
        self.config = config or self._default_config()
        self.model_version = "1.0"
        self.risk_thresholds = {
            "low": 0.3,
            "medium": 0.6,
            "high": 0.8,
            "critical": 0.95
        }
    
    def _default_config(self) -> Dict[str, Any]:
        """Get default fraud detection configuration."""
        return {
            "max_daily_amount": 10000.00,
            "max_transaction_amount": 5000.00,
            "suspicious_locations": ["high_risk_country_codes"],
            "velocity_check_window_minutes": 30,
            "max_transactions_per_window": 5
        }
    
    def analyze_transaction(self, transaction: Transaction, 
                          customer_history: List[Transaction] = None) -> FraudScore:
        """
        Analyze transaction for fraud indicators.
        
        Args:
            transaction: Transaction to analyze
            customer_history: Recent customer transaction history
            
        Returns:
            Fraud score and recommendation
        """
        customer_history = customer_history or []
        
        # Calculate individual risk factors
        amount_score = self._analyze_amount_risk(transaction, customer_history)
        location_score = self._analyze_location_risk(transaction, customer_history)
        velocity_score = self._analyze_velocity_risk(transaction, customer_history)
        pattern_score = self._analyze_pattern_risk(transaction, customer_history)
        
        # Weighted composite score
        composite_score = (
            amount_score * 0.3 +
            location_score * 0.2 +
            velocity_score * 0.3 +
            pattern_score * 0.2
        )
        
        # Determine risk level and recommendation
        risk_level = self._determine_risk_level(composite_score)
        recommendation = self._get_recommendation(risk_level, composite_score)
        
        # Collect contributing factors
        factors = self._identify_risk_factors(
            amount_score, location_score, velocity_score, pattern_score
        )
        
        return FraudScore(
            transaction_id=transaction.id,
            score=composite_score,
            risk_level=risk_level,
            factors=factors,
            recommendation=recommendation
        )
    
    def _analyze_amount_risk(self, transaction: Transaction, 
                           history: List[Transaction]) -> float:
        """Analyze transaction amount risk."""
        amount = float(transaction.amount)
        
        # Check against absolute limits
        if amount > self.config["max_transaction_amount"]:
            return 0.9
        
        # Check against customer's historical patterns
        if history:
            historical_amounts = [float(t.amount) for t in history[-10:]]
            avg_amount = sum(historical_amounts) / len(historical_amounts)
            
            # Unusual amount deviation
            if amount > avg_amount * 3:
                return 0.7
            elif amount > avg_amount * 2:
                return 0.4
        
        # Check daily spending
        today_total = sum(
            float(t.amount) for t in history
            if t.timestamp.date() == transaction.timestamp.date()
        )
        
        if today_total + amount > self.config["max_daily_amount"]:
            return 0.8
        
        return 0.1
    
    def _analyze_location_risk(self, transaction: Transaction, 
                             history: List[Transaction]) -> float:
        """Analyze transaction location risk."""
        location = transaction.location.lower()
        
        # Check suspicious locations
        for suspicious in self.config["suspicious_locations"]:
            if suspicious.lower() in location:
                return 0.9
        
        # Check against customer's usual locations
        if history:
            usual_locations = set(t.location.lower() for t in history[-20:])
            if location not in usual_locations:
                return 0.6
        
        return 0.1
    
    def _analyze_velocity_risk(self, transaction: Transaction, 
                             history: List[Transaction]) -> float:
        """Analyze transaction velocity risk."""
        # Count recent transactions in time window
        window_start = transaction.timestamp.replace(
            minute=transaction.timestamp.minute - self.config["velocity_check_window_minutes"]
        )
        
        recent_transactions = [
            t for t in history
            if t.timestamp >= window_start and t.timestamp <= transaction.timestamp
        ]
        
        if len(recent_transactions) >= self.config["max_transactions_per_window"]:
            return 0.8
        elif len(recent_transactions) >= self.config["max_transactions_per_window"] * 0.7:
            return 0.5
        
        return 0.1
    
    def _analyze_pattern_risk(self, transaction: Transaction, 
                            history: List[Transaction]) -> float:
        """Analyze transaction pattern anomalies."""
        # Check for unusual merchant categories
        if history:
            historical_merchants = set(t.merchant.lower() for t in history[-15:])
            if transaction.merchant.lower() not in historical_merchants:
                return 0.4
        
        # Check for unusual transaction times
        hour = transaction.timestamp.hour
        if hour < 6 or hour > 22:  # Late night/early morning
            return 0.3
        
        return 0.1
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level from composite score."""
        if score >= self.risk_thresholds["critical"]:
            return "CRITICAL"
        elif score >= self.risk_thresholds["high"]:
            return "HIGH"
        elif score >= self.risk_thresholds["medium"]:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_recommendation(self, risk_level: str, score: float) -> str:
        """Get action recommendation based on risk level."""
        recommendations = {
            "LOW": "APPROVE",
            "MEDIUM": "REVIEW",
            "HIGH": "DECLINE",
            "CRITICAL": "BLOCK_CARD"
        }
        return recommendations.get(risk_level, "REVIEW")
    
    def _identify_risk_factors(self, amount_score: float, location_score: float,
                             velocity_score: float, pattern_score: float) -> List[str]:
        """Identify contributing risk factors."""
        factors = []
        
        if amount_score > 0.5:
            factors.append("Unusual transaction amount")
        if location_score > 0.5:
            factors.append("Suspicious or unusual location")
        if velocity_score > 0.5:
            factors.append("High transaction velocity")
        if pattern_score > 0.5:
            factors.append("Unusual transaction pattern")
        
        return factors
'''
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Generated fraud detection model: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error generating fraud detection model: {e}")
            return None
    
    def _create_transaction_monitor(self) -> Optional[str]:
        """Create transaction monitoring service."""
        try:
            filepath = self.mybank_root / "fraud_detection" / "transaction_monitor.py"
            
            content = '''"""
Real-Time Transaction Monitor for MyBank

Monitors all transactions in real-time for fraud detection.
Generated by Code Agent
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass

try:
    from .fraud_detector import FraudDetector, Transaction, FraudScore
except ImportError:
    # Fallback for standalone usage
    FraudDetector = None
    Transaction = None
    FraudScore = None

logger = logging.getLogger(__name__)


@dataclass
class MonitoringAlert:
    """Alert generated by transaction monitoring."""
    alert_id: str
    transaction_id: str
    customer_id: str
    alert_type: str
    severity: str
    message: str
    timestamp: datetime
    fraud_score: float
    recommended_action: str


class TransactionMonitor:
    """
    Real-time transaction monitoring service with fraud detection.
    """
    
    def __init__(self, fraud_detector: FraudDetector = None):
        """Initialize transaction monitor."""
        self.fraud_detector = fraud_detector or FraudDetector()
        self.alert_handlers: List[Callable] = []
        self.monitoring_active = False
        self.processed_count = 0
        self.alert_count = 0
        self.logger = logger
    
    def add_alert_handler(self, handler: Callable[[MonitoringAlert], None]):
        """Add alert handler callback."""
        self.alert_handlers.append(handler)
    
    def start_monitoring(self):
        """Start real-time transaction monitoring."""
        self.monitoring_active = True
        self.logger.info("Transaction monitoring started")
    
    def stop_monitoring(self):
        """Stop transaction monitoring."""
        self.monitoring_active = False
        self.logger.info("Transaction monitoring stopped")
    
    async def process_transaction(self, transaction_data: Dict[str, Any], 
                                customer_history: List[Dict[str, Any]] = None) -> MonitoringAlert:
        """
        Process a single transaction for fraud detection.
        
        Args:
            transaction_data: Transaction details
            customer_history: Recent customer transaction history
            
        Returns:
            Monitoring alert if generated
        """
        if not self.monitoring_active:
            return None
        
        try:
            # Convert to Transaction object
            transaction = self._dict_to_transaction(transaction_data)
            
            # Convert history if provided
            history = []
            if customer_history:
                history = [self._dict_to_transaction(t) for t in customer_history]
            
            # Analyze for fraud
            fraud_score = self.fraud_detector.analyze_transaction(transaction, history)
            
            # Generate alert if necessary
            alert = self._generate_alert_if_needed(transaction, fraud_score)
            
            # Increment processed count
            self.processed_count += 1
            
            # Log processing
            self.logger.debug(
                f"Processed transaction {transaction.id}: "
                f"score={fraud_score.score:.3f}, level={fraud_score.risk_level}"
            )
            
            # Send alerts to handlers
            if alert:
                await self._send_alert(alert)
            
            return alert
            
        except Exception as e:
            self.logger.error(f"Error processing transaction: {e}")
            raise
    
    def _dict_to_transaction(self, data: Dict[str, Any]) -> Transaction:
        """Convert dictionary to Transaction object."""
        return Transaction(
            id=data["id"],
            customer_id=data["customer_id"],
            amount=data["amount"],
            merchant=data["merchant"],
            location=data["location"],
            timestamp=data.get("timestamp", datetime.now()),
            card_number_hash=data["card_number_hash"],
            transaction_type=data["transaction_type"],
            metadata=data.get("metadata", {})
        )
    
    def _generate_alert_if_needed(self, transaction: Transaction, 
                                fraud_score: FraudScore) -> Optional[MonitoringAlert]:
        """Generate monitoring alert if thresholds are met."""
        # Only alert on medium risk and above
        if fraud_score.risk_level in ["MEDIUM", "HIGH", "CRITICAL"]:
            alert = MonitoringAlert(
                alert_id=f"ALERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{transaction.id}",
                transaction_id=transaction.id,
                customer_id=transaction.customer_id,
                alert_type="FRAUD_RISK",
                severity=fraud_score.risk_level,
                message=f"Fraud risk detected: {', '.join(fraud_score.factors)}",
                timestamp=datetime.now(),
                fraud_score=fraud_score.score,
                recommended_action=fraud_score.recommendation
            )
            
            self.alert_count += 1
            return alert
        
        return None
    
    async def _send_alert(self, alert: MonitoringAlert):
        """Send alert to all registered handlers."""
        for handler in self.alert_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(alert)
                else:
                    handler(alert)
            except Exception as e:
                self.logger.error(f"Error in alert handler: {e}")
    
    def get_monitoring_stats(self) -> Dict[str, Any]:
        """Get current monitoring statistics."""
        return {
            "monitoring_active": self.monitoring_active,
            "processed_transactions": self.processed_count,
            "alerts_generated": self.alert_count,
            "alert_rate": self.alert_count / max(self.processed_count, 1),
            "uptime": "active" if self.monitoring_active else "stopped"
        }
    
    async def bulk_process_transactions(self, transactions: List[Dict[str, Any]]) -> List[MonitoringAlert]:
        """Process multiple transactions in batch."""
        alerts = []
        
        for transaction_data in transactions:
            alert = await self.process_transaction(transaction_data)
            if alert:
                alerts.append(alert)
        
        self.logger.info(f"Bulk processed {len(transactions)} transactions, generated {len(alerts)} alerts")
        return alerts


# Example alert handlers
def console_alert_handler(alert: MonitoringAlert):
    """Simple console alert handler."""
    print(f"🚨 FRAUD ALERT: {alert.severity} risk for transaction {alert.transaction_id}")
    print(f"   Customer: {alert.customer_id}")
    print(f"   Score: {alert.fraud_score:.3f}")
    print(f"   Recommendation: {alert.recommended_action}")
    print(f"   Message: {alert.message}")


async def async_alert_handler(alert: MonitoringAlert):
    """Async alert handler for external system integration."""
    # Simulate external system call
    await asyncio.sleep(0.1)
    logger.info(f"Sent alert {alert.alert_id} to external fraud management system")
'''
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Generated transaction monitor: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error generating transaction monitor: {e}")
            return None
    
    def _create_alert_system(self) -> Optional[str]:
        """Create fraud alert system."""
        try:
            filepath = self.mybank_root / "fraud_detection" / "alert_system.py"
            
            content = '''"""
Fraud Alert System for MyBank

Customer notification and alert management system.
Generated by Code Agent
"""
import smtplib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from .transaction_monitor import MonitoringAlert
except ImportError:
    MonitoringAlert = None


@dataclass
class Customer:
    """Customer information for alerts."""
    customer_id: str
    email: str
    phone: str
    name: str
    alert_preferences: Dict[str, bool]


@dataclass
class AlertDelivery:
    """Alert delivery tracking."""
    delivery_id: str
    alert_id: str
    customer_id: str
    channel: str  # EMAIL, SMS, PUSH, PHONE
    status: str  # PENDING, SENT, DELIVERED, FAILED
    timestamp: datetime
    retry_count: int = 0


class FraudAlertSystem:
    """
    Customer fraud alert and notification system.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize alert system."""
        self.config = config or self._default_config()
        self.delivery_log: List[AlertDelivery] = []
        self.customer_cache: Dict[str, Customer] = {}
    
    def _default_config(self) -> Dict[str, Any]:
        """Get default alert system configuration."""
        return {
            "smtp_server": "localhost",
            "smtp_port": 587,
            "email_from": "fraud-alerts@mybank.com",
            "sms_provider": "twilio",
            "max_retries": 3,
            "retry_delay_minutes": 5,
            "alert_timeout_hours": 24
        }
    
    async def send_fraud_alert(self, alert: MonitoringAlert, 
                             customer: Customer) -> List[AlertDelivery]:
        """
        Send fraud alert to customer via preferred channels.
        
        Args:
            alert: Fraud monitoring alert
            customer: Customer information
            
        Returns:
            List of delivery attempts
        """
        deliveries = []
        
        # Determine alert urgency and channels
        channels = self._get_alert_channels(alert.severity, customer.alert_preferences)
        
        # Send via each channel
        for channel in channels:
            delivery = await self._send_via_channel(alert, customer, channel)
            deliveries.append(delivery)
            self.delivery_log.append(delivery)
        
        return deliveries
    
    def _get_alert_channels(self, severity: str, preferences: Dict[str, bool]) -> List[str]:
        """Determine which channels to use based on severity and preferences."""
        channels = []
        
        # Always use email for any fraud alert
        if preferences.get("email", True):
            channels.append("EMAIL")
        
        # SMS for high severity
        if severity in ["HIGH", "CRITICAL"] and preferences.get("sms", True):
            channels.append("SMS")
        
        # Push notifications if available
        if preferences.get("push", True):
            channels.append("PUSH")
        
        # Phone call for critical alerts
        if severity == "CRITICAL" and preferences.get("phone", False):
            channels.append("PHONE")
        
        return channels
    
    async def _send_via_channel(self, alert: MonitoringAlert, 
                              customer: Customer, channel: str) -> AlertDelivery:
        """Send alert via specific channel."""
        delivery = AlertDelivery(
            delivery_id=f"{channel}_{alert.alert_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            alert_id=alert.alert_id,
            customer_id=customer.customer_id,
            channel=channel,
            status="PENDING",
            timestamp=datetime.now()
        )
        
        try:
            if channel == "EMAIL":
                success = await self._send_email_alert(alert, customer)
            elif channel == "SMS":
                success = await self._send_sms_alert(alert, customer)
            elif channel == "PUSH":
                success = await self._send_push_alert(alert, customer)
            elif channel == "PHONE":
                success = await self._send_phone_alert(alert, customer)
            else:
                success = False
            
            delivery.status = "SENT" if success else "FAILED"
            
        except Exception as e:
            delivery.status = "FAILED"
            print(f"Error sending {channel} alert: {e}")
        
        return delivery
    
    async def _send_email_alert(self, alert: MonitoringAlert, customer: Customer) -> bool:
        """Send fraud alert via email."""
        try:
            # Create email content
            subject = f"🚨 MyBank Fraud Alert - {alert.severity} Risk Detected"
            
            html_body = f"""
            <html>
            <body>
                <h2 style="color: #d32f2f;">MyBank Security Alert</h2>
                <p>Dear {customer.name},</p>
                
                <p>We've detected suspicious activity on your account and have taken protective measures.</p>
                
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3>Alert Details:</h3>
                    <p><strong>Severity:</strong> {alert.severity}</p>
                    <p><strong>Alert ID:</strong> {alert.alert_id}</p>
                    <p><strong>Time:</strong> {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Recommended Action:</strong> {alert.recommended_action}</p>
                </div>
                
                <p><strong>What you should do:</strong></p>
                <ul>
                    <li>Review your recent transactions</li>
                    <li>Contact us immediately if you don't recognize this activity</li>
                    <li>Do not ignore this alert</li>
                </ul>
                
                <p>If this was you, no action is needed. If not, please contact our fraud department immediately at 1-800-MYBANK-FRAUD.</p>
                
                <p>Best regards,<br>MyBank Security Team</p>
                
                <p style="font-size: 12px; color: #666;">
                    This is an automated security alert. Please do not reply to this email.
                </p>
            </body>
            </html>
            """
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config['email_from']
            msg['To'] = customer.email
            
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Send email (simplified - would use actual SMTP in production)
            print(f"📧 EMAIL ALERT sent to {customer.email}: {subject}")
            return True
            
        except Exception as e:
            print(f"Failed to send email alert: {e}")
            return False
    
    async def _send_sms_alert(self, alert: MonitoringAlert, customer: Customer) -> bool:
        """Send fraud alert via SMS."""
        try:
            message = (
                f"🚨 MyBank FRAUD ALERT: {alert.severity} risk detected on your account. "
                f"Action: {alert.recommended_action}. "
                f"If this wasn't you, call 1-800-MYBANK-FRAUD immediately. Alert ID: {alert.alert_id}"
            )
            
            # Send SMS (simplified - would use actual SMS service in production)
            print(f"📱 SMS ALERT sent to {customer.phone}: {message[:100]}...")
            return True
            
        except Exception as e:
            print(f"Failed to send SMS alert: {e}")
            return False
    
    async def _send_push_alert(self, alert: MonitoringAlert, customer: Customer) -> bool:
        """Send fraud alert via push notification."""
        try:
            push_data = {
                "title": "🚨 MyBank Fraud Alert",
                "body": f"{alert.severity} risk detected. Tap for details.",
                "data": {
                    "alert_id": alert.alert_id,
                    "severity": alert.severity,
                    "action": alert.recommended_action
                }
            }
            
            # Send push notification (simplified - would use actual push service)
            print(f"🔔 PUSH ALERT sent to customer {customer.customer_id}: {push_data['title']}")
            return True
            
        except Exception as e:
            print(f"Failed to send push alert: {e}")
            return False
    
    async def _send_phone_alert(self, alert: MonitoringAlert, customer: Customer) -> bool:
        """Send fraud alert via automated phone call."""
        try:
            call_script = (
                f"Hello, this is MyBank security. We've detected {alert.severity.lower()} risk "
                f"activity on your account. Please call us immediately at 1-800-MYBANK-FRAUD "
                f"to verify your recent transactions. Alert reference: {alert.alert_id}."
            )
            
            # Make automated call (simplified - would use actual phone service)
            print(f"📞 PHONE ALERT initiated to {customer.phone}: {call_script[:50]}...")
            return True
            
        except Exception as e:
            print(f"Failed to send phone alert: {e}")
            return False
    
    def get_delivery_status(self, alert_id: str) -> List[AlertDelivery]:
        """Get delivery status for an alert."""
        return [d for d in self.delivery_log if d.alert_id == alert_id]
    
    def get_customer_alert_history(self, customer_id: str) -> List[AlertDelivery]:
        """Get alert history for a customer."""
        return [d for d in self.delivery_log if d.customer_id == customer_id]
'''
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Generated alert system: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error generating alert system: {e}")
            return None
    
    def commit_changes(self, generation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Commit generated code changes to Git."""
        try:
            import subprocess
            
            files_to_commit = generation_result.get("generated_files", []) + generation_result.get("updated_files", [])
            
            if not files_to_commit:
                return {"status": "no_changes", "message": "No files to commit"}
            
            # Add files to git
            for file_path in files_to_commit:
                subprocess.run(["git", "add", file_path], cwd=project_root, check=True)
            
            # Create commit message
            commit_message = f"Generated code via Code Agent - {generation_result.get('generation_type', 'unknown')}"
            
            # Commit changes
            result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    "status": "committed",
                    "commit_hash": result.stdout.strip(),
                    "message": commit_message,
                    "files_committed": len(files_to_commit)
                }
            else:
                return {
                    "status": "commit_failed",
                    "error": result.stderr,
                    "files_staged": len(files_to_commit)
                }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Failed to commit changes"
            }
    
    def get_code_agent_status(self) -> Dict[str, Any]:
        """Get current code agent status."""
        return {
            "agent_id": self.agent_id,
            "version": self.version,
            "status": "active",
            "mybank_root": str(self.mybank_root),
            "supported_actions": ["generate_code_snippet", "commit_changes"],
            "inputs": ["specs/stories/**", "src/MyBank/**"],
            "outputs": ["src/MyBank/**"],
            "banking_domains_supported": [
                "accounts", "loans", "credit_cards", "payments", 
                "investments", "fraud_detection", "compliance"
            ],
            "patterns_supported": ["repository", "service", "model", "api"]
        }


def main():
    """CLI interface for the code agent."""
    import argparse
    
    parser = argparse.ArgumentParser(description="PromptToProduct Code Agent")
    parser.add_argument("prompt", nargs="?", help="Code generation prompt")
    parser.add_argument("--status", action="store_true", help="Show code agent status")
    parser.add_argument("--init", action="store_true", help="Initialize MyBank structure")
    args = parser.parse_args()
    
    # Initialize code agent
    code_agent = CodeAgent()
    
    if args.status:
        status = code_agent.get_code_agent_status()
        print("💻 Code Agent Status")
        print("=" * 40)
        for key, value in status.items():
            print(f"{key}: {value}")
        return
    
    if args.init:
        code_agent._initialize_mybank_structure()
        print("✅ MyBank directory structure initialized")
        return
    
    if not args.prompt:
        print("Usage: python code_agent.py '<prompt>' or --status or --init")
        return
    
    # Prepare agent parameters (simulating orchestrator input)
    agent_params = {
        "prompt": args.prompt,
        "banking_context": {"is_banking": True, "product_types": ["credit_cards"], "compliance_areas": []},
        "entities": {"technologies": [], "epic_references": [], "feature_references": []}
    }
    
    # Generate code
    print(f"💻 Processing: {args.prompt}")
    print("-" * 50)
    
    result = code_agent.generate_code_from_specs(agent_params)
    
    # Display results
    print(f"✅ Generation Type: {result.get('generation_type', 'unknown')}")
    print(f"📁 Files Generated: {len(result.get('generated_files', []))}")
    
    for file_path in result.get('generated_files', []):
        print(f"   📄 {file_path}")
    
    if result.get('commit_info'):
        commit_info = result['commit_info']
        print(f"📝 Commit Status: {commit_info.get('status', 'unknown')}")
    
    if result.get('errors'):
        print(f"❌ Errors: {', '.join(result['errors'])}")
    
    print(f"📊 Status: {result.get('status', 'unknown')}")


if __name__ == "__main__":
    main()