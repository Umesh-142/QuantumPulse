// Custom JavaScript for enhanced interactivity
document.addEventListener("DOMContentLoaded", function () {
  console.log("Quantum Data Generator - Enhanced UI Loaded");

  // Add smooth scrolling
  const links = document.querySelectorAll('a[href^="#"]');
  links.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Add fade-in animation to results
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("fadeInUp");
      }
    });
  });

  // Observe results containers
  const resultsContainers = document.querySelectorAll(".results-container");
  resultsContainers.forEach((container) => {
    observer.observe(container);
  });

  // Enhanced button click effects
  const buttons = document.querySelectorAll(".stButton > button");
  buttons.forEach((button) => {
    button.addEventListener("click", function () {
      this.style.transform = "scale(0.98)";
      setTimeout(() => {
        this.style.transform = "";
      }, 150);
    });
  });

  // Real-time parameter validation
  const sliders = document.querySelectorAll(".stSlider");
  sliders.forEach((slider) => {
    slider.addEventListener("input", function () {
      // Add visual feedback for parameter changes
      this.style.boxShadow = "0 0 10px rgba(102, 126, 234, 0.3)";
      setTimeout(() => {
        this.style.boxShadow = "";
      }, 300);
    });
  });

  // Tooltip system for complex parameters
  function addTooltips() {
    const tooltipTriggers = document.querySelectorAll("[data-tooltip]");
    tooltipTriggers.forEach((trigger) => {
      const tooltip = document.createElement("div");
      tooltip.className = "custom-tooltip";
      tooltip.textContent = trigger.getAttribute("data-tooltip");

      trigger.addEventListener("mouseenter", function () {
        document.body.appendChild(tooltip);
        const rect = trigger.getBoundingClientRect();
        tooltip.style.left = rect.left + "px";
        tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + "px";
        tooltip.style.opacity = "1";
      });

      trigger.addEventListener("mouseleave", function () {
        if (tooltip.parentNode) {
          tooltip.parentNode.removeChild(tooltip);
        }
      });
    });
  }

  // Initialize tooltips
  addTooltips();

  // Progress indicator for data generation
  function showProgress() {
    const progressBar = document.createElement("div");
    progressBar.className = "progress-bar";
    progressBar.innerHTML = `
            <div class="progress-fill"></div>
            <span class="progress-text">Generating quantum data...</span>
        `;
    return progressBar;
  }

  // Enhanced error handling
  window.addEventListener("error", function (e) {
    console.error("Application Error:", e.error);
    // Could add user-friendly error notifications here
  });

  // Keyboard shortcuts
  document.addEventListener("keydown", function (e) {
    // Ctrl+G to generate data
    if (e.ctrlKey && e.key === "g") {
      e.preventDefault();
      const generateButton = document.querySelector(".stButton > button");
      if (generateButton && generateButton.textContent.includes("Generate")) {
        generateButton.click();
      }
    }

    // Ctrl+D to download
    if (e.ctrlKey && e.key === "d") {
      e.preventDefault();
      const downloadButton = document.querySelector('button[kind="secondary"]');
      if (downloadButton) {
        downloadButton.click();
      }
    }
  });

  // Auto-save parameters to localStorage
  function saveParameters() {
    const params = {};
    const inputs = document.querySelectorAll("input, select");
    inputs.forEach((input) => {
      if (input.name) {
        params[input.name] = input.value;
      }
    });
    localStorage.setItem("quantumGeneratorParams", JSON.stringify(params));
  }

  // Load saved parameters
  function loadParameters() {
    const saved = localStorage.getItem("quantumGeneratorParams");
    if (saved) {
      const params = JSON.parse(saved);
      Object.keys(params).forEach((key) => {
        const input = document.querySelector(`[name="${key}"]`);
        if (input) {
          input.value = params[key];
        }
      });
    }
  }

  // Initialize parameter persistence
  loadParameters();
  document.addEventListener("input", saveParameters);
});

// CSS for custom tooltips and progress bar
const customStyles = `
<style>
.custom-tooltip {
    position: absolute;
    background: rgba(0, 0, 0, 0.9);
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 12px;
    z-index: 1000;
    opacity: 0;
    transition: opacity 0.3s;
    pointer-events: none;
    max-width: 200px;
    word-wrap: break-word;
}

.progress-bar {
    position: fixed;
    top: 20px;
    right: 20px;
    background: white;
    padding: 15px 20px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    z-index: 1000;
    min-width: 250px;
}

.progress-fill {
    height: 4px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    border-radius: 2px;
    animation: progressFill 3s ease-in-out;
}

.progress-text {
    display: block;
    margin-top: 8px;
    font-size: 14px;
    color: #333;
    font-weight: 500;
}

@keyframes progressFill {
    0% { width: 0%; }
    50% { width: 70%; }
    100% { width: 100%; }
}
</style>
`;

document.head.insertAdjacentHTML("beforeend", customStyles);
