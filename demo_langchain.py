#!/usr/bin/env python3
"""
Demo script to test the LangChain-enhanced AutoAgent platform
"""

import asyncio
import json
import os
from app.orchestrator.task_manager import TaskManager

async def demo_langchain_agents():
    """Demo the LangChain-enhanced agent system"""
    print("🚗 AutoAgent LangChain Demo")
    print("=" * 50)
    
    # Initialize task manager
    task_manager = TaskManager()
    
    # Demo query
    demo_query = "Best EV under ₹15L in Delhi?"
    print(f"🎯 Demo Query: {demo_query}")
    print()
    
    try:
        # Process the query
        result = await task_manager.orchestrate_task(
            user_query=demo_query,
            context={"demo_mode": True, "langchain_enabled": True}
        )
        
        print("📊 Results:")
        print("-" * 30)
        
        # Display agent trace
        print("🤖 Agent Execution Trace:")
        for trace in result["agent_trace"]:
            print(f"  • {trace.agent}: {trace.output}")
        
        print()
        
        # Display final result summary
        final_result = result["result"]
        print("🎯 Final Result:")
        print(f"  Query: {final_result.get('query', 'N/A')}")
        print(f"  Cars Found: {len(final_result.get('cars', []))}")
        print(f"  Summary: {final_result.get('summary', 'N/A')}")
        
        # Display cars if found
        cars = final_result.get("cars", [])
        if cars:
            print("\n🚙 Cars Found:")
            for i, car in enumerate(cars, 1):
                print(f"  {i}. {car['make']} {car['model']}")
                print(f"     Price: ₹{car['price']//100000}L")
                print(f"     Rating: {car['rating']}/5")
                if 'features' in car:
                    print(f"     Features: {', '.join(car['features'][:2])}")
                print()
        
        # Display insights if available
        insights = final_result.get("insights", [])
        if insights:
            print("💡 Market Insights:")
            for insight in insights[:3]:  # Show top 3 insights
                print(f"  • {insight.get('title', 'Insight')}: {insight.get('content', 'N/A')}")
            print()
        
        # Check if LangChain was used
        if final_result.get("langchain_used"):
            print("✅ LangChain integration active")
        else:
            print("⚠️  Using fallback mode (LangChain not available or no API key)")
        
        print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("This might be due to missing dependencies or API keys")

def check_environment():
    """Check if environment is properly set up"""
    print("🔍 Environment Check:")
    print("-" * 20)
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OpenAI API key found")
    else:
        print("⚠️  OpenAI API key not found (set OPENAI_API_KEY environment variable)")
        print("   Demo will run in fallback mode")
    
    # Check for LangChain
    try:
        import langchain
        print("✅ LangChain available")
    except ImportError:
        print("⚠️  LangChain not installed (pip install -r requirements.txt)")
    
    # Check for FastAPI
    try:
        import fastapi
        print("✅ FastAPI available")
    except ImportError:
        print("❌ FastAPI not installed")
    
    print()

async def interactive_demo():
    """Interactive demo where user can ask questions"""
    print("🎮 Interactive Demo Mode")
    print("Type 'quit' to exit")
    print("-" * 30)
    
    task_manager = TaskManager()
    
    while True:
        try:
            query = input("\n🤔 Ask me about cars: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            print(f"\n🔄 Processing: {query}")
            
            result = await task_manager.orchestrate_task(
                user_query=query,
                context={"interactive_mode": True}
            )
            
            final_result = result["result"]
            print(f"\n💬 Response: {final_result.get('summary', 'No summary available')}")
            
            # Show cars if found
            cars = final_result.get("cars", [])
            if cars:
                print(f"\n🚗 Found {len(cars)} cars:")
                for car in cars:
                    print(f"  • {car['make']} {car['model']} - ₹{car['price']//100000}L")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚗 AutoAgent LangChain Demo")
    print("=" * 50)
    
    # Check environment
    check_environment()
    
    # Choose demo mode
    print("Choose demo mode:")
    print("1. Automated demo")
    print("2. Interactive demo")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            asyncio.run(demo_langchain_agents())
        elif choice == "2":
            asyncio.run(interactive_demo())
        else:
            print("Invalid choice, running automated demo...")
            asyncio.run(demo_langchain_agents())
            
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled")
    except Exception as e:
        print(f"❌ Demo error: {str(e)}")