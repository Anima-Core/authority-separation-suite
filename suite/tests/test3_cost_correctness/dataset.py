"""
Dataset generation for cost-correctness test
"""
import json
import os
import random
from typing import List, Dict, Any

class CostCorrectnessDataset:
    def __init__(self, seed: int = 42, quick_mode: bool = False):
        random.seed(seed)
        self.quick_mode = quick_mode
        self.templates = self._create_templates()
        self.tasks = self._generate_tasks()
    
    def _create_templates(self) -> Dict[str, Dict[str, Any]]:
        """Create response templates for common task categories"""
        
        templates = {
            "billing_inquiry": {
                "template": "Thank you for contacting us about your billing inquiry. Your account balance is ${balance}. Your next payment of ${amount} is due on {due_date}. If you have questions, please contact our billing department at billing@company.com.",
                "fields": ["balance", "amount", "due_date"],
                "category": "billing"
            },
            "password_reset": {
                "template": "We've received your password reset request for account {username}. Please check your email at {email} for reset instructions. The reset link will expire in 24 hours. If you didn't request this reset, please contact security@company.com immediately.",
                "fields": ["username", "email"],
                "category": "account"
            },
            "shipping_status": {
                "template": "Your order #{order_id} shipped on {ship_date} via {carrier}. Tracking number: {tracking}. Estimated delivery: {delivery_date}. You can track your package at {tracking_url}.",
                "fields": ["order_id", "ship_date", "carrier", "tracking", "delivery_date", "tracking_url"],
                "category": "shipping"
            },
            "refund_request": {
                "template": "Your refund request for order #{order_id} has been processed. Refund amount: ${amount}. Please allow 3-5 business days for the refund to appear on your {payment_method}. Reference number: {ref_number}.",
                "fields": ["order_id", "amount", "payment_method", "ref_number"],
                "category": "refund"
            },
            "technical_support": {
                "template": "Thank you for contacting technical support regarding {issue_type}. Based on your description, please try the following steps: {solution_steps}. If the issue persists, please reply with error code {error_code} and we'll escalate to our engineering team.",
                "fields": ["issue_type", "solution_steps", "error_code"],
                "category": "technical"
            }
        }
        
        return templates
    
    def _generate_tasks(self) -> List[Dict[str, Any]]:
        """Generate workflow tasks that can be solved with templates"""
        
        tasks = []
        
        # Billing inquiries
        billing_tasks = [
            {
                "task_id": "task_1",
                "category": "billing",
                "template_id": "billing_inquiry",
                "description": "Customer asking about account balance and next payment due date",
                "input_data": {
                    "customer_message": "Hi, I need to check my account balance and when my next payment is due. My account number is 12345.",
                    "account_info": {"balance": "156.78", "amount": "89.99", "due_date": "March 15, 2024"}
                },
                "expected_fields": {"balance": "156.78", "amount": "89.99", "due_date": "March 15, 2024"}
            },
            {
                "task_id": "task_2", 
                "category": "billing",
                "template_id": "billing_inquiry",
                "description": "Customer questioning a charge on their bill",
                "input_data": {
                    "customer_message": "I see a charge of $45.99 on my bill that I don't recognize. Can you help?",
                    "account_info": {"balance": "245.99", "amount": "45.99", "due_date": "April 1, 2024"}
                },
                "expected_fields": {"balance": "245.99", "amount": "45.99", "due_date": "April 1, 2024"}
            }
        ]
        
        # Account issues
        account_tasks = [
            {
                "task_id": "task_3",
                "category": "account", 
                "template_id": "password_reset",
                "description": "Customer needs password reset",
                "input_data": {
                    "customer_message": "I forgot my password and can't log in. My username is john_doe.",
                    "account_info": {"username": "john_doe", "email": "john.doe@email.com"}
                },
                "expected_fields": {"username": "john_doe", "email": "john.doe@email.com"}
            }
        ]
        
        # Shipping inquiries
        shipping_tasks = [
            {
                "task_id": "task_4",
                "category": "shipping",
                "template_id": "shipping_status", 
                "description": "Customer asking about order status",
                "input_data": {
                    "customer_message": "Where is my order? Order number is ORD-789.",
                    "order_info": {
                        "order_id": "ORD-789",
                        "ship_date": "March 10, 2024",
                        "carrier": "FedEx",
                        "tracking": "1234567890",
                        "delivery_date": "March 13, 2024",
                        "tracking_url": "fedex.com/tracking"
                    }
                },
                "expected_fields": {
                    "order_id": "ORD-789",
                    "ship_date": "March 10, 2024", 
                    "carrier": "FedEx",
                    "tracking": "1234567890",
                    "delivery_date": "March 13, 2024",
                    "tracking_url": "fedex.com/tracking"
                }
            }
        ]
        
        # Technical support
        technical_tasks = [
            {
                "task_id": "task_5",
                "category": "technical",
                "template_id": "technical_support",
                "description": "Customer reporting login issues",
                "input_data": {
                    "customer_message": "I keep getting an error when trying to log in. It says 'connection timeout'.",
                    "issue_info": {
                        "issue_type": "login timeout",
                        "solution_steps": "1. Clear browser cache 2. Try incognito mode 3. Check internet connection",
                        "error_code": "ERR_TIMEOUT_001"
                    }
                },
                "expected_fields": {
                    "issue_type": "login timeout",
                    "solution_steps": "1. Clear browser cache 2. Try incognito mode 3. Check internet connection", 
                    "error_code": "ERR_TIMEOUT_001"
                }
            }
        ]
        
        tasks.extend(billing_tasks)
        tasks.extend(account_tasks)
        tasks.extend(shipping_tasks)
        tasks.extend(technical_tasks)
        
        # Add some tasks without clear templates (for free-form responses)
        freeform_tasks = [
            {
                "task_id": "task_6",
                "category": "general",
                "template_id": None,
                "description": "Complex customer complaint requiring personalized response",
                "input_data": {
                    "customer_message": "I'm very frustrated with the service. This is the third time I've had issues and nobody seems to care. I've been a loyal customer for 5 years and I'm considering switching to a competitor."
                },
                "expected_fields": None
            }
        ]
        
        tasks.extend(freeform_tasks)
        
        # Shuffle and limit for quick mode
        random.shuffle(tasks)
        if self.quick_mode:
            tasks = tasks[:3]
        
        return tasks
    
    def get_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get response templates"""
        return self.templates
    
    def get_tasks(self) -> List[Dict[str, Any]]:
        """Get task dataset"""
        return self.tasks
    
    def render_template(self, template_id: str, fields: Dict[str, str]) -> str:
        """Render a template with provided fields"""
        if template_id not in self.templates:
            return f"Template {template_id} not found"
        
        template = self.templates[template_id]
        response = template['template']
        
        # Replace field placeholders
        for field, value in fields.items():
            placeholder = "{" + field + "}"
            response = response.replace(placeholder, str(value))
        
        return response
    
    def save_dataset(self, output_dir: str):
        """Save dataset to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save templates
        templates_path = os.path.join(output_dir, "templates.json")
        with open(templates_path, 'w') as f:
            json.dump(self.templates, f, indent=2)
        
        # Save tasks
        tasks_path = os.path.join(output_dir, "tasks.json")
        with open(tasks_path, 'w') as f:
            json.dump(self.tasks, f, indent=2)
        
        print(f"Cost-correctness dataset saved to {output_dir}")
        return templates_path, tasks_path