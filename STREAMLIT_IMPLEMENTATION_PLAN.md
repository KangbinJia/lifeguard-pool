# Streamlit Implementation Plan

This file describes the phased plan for adding a Streamlit web implementation alongside the existing Pygame simulation.

## Goal

Keep the current Pygame solution unchanged, and add a new Streamlit-based implementation in separate files so the project can be run as a web app.

## Phases

### Phase 1: Plan and scaffold
- Create a dedicated implementation plan file.
- Define the required new files and their responsibilities.
- Ensure the Pygame files remain unchanged.

### Phase 2: Setup Streamlit entrypoint
- Add `streamlit_app.py` as the main app file.
- Add `requirements.txt` containing Streamlit and any plotting dependencies.
- Update `README.md` with instructions for running the Streamlit app.

### Phase 3: Translate simulation logic
- Port the core lifeguard/geography model from Python/Pygame to a logic layer usable by Streamlit.
- Keep the same pool geometry, target generation, and optimal entry computation.
- Expose functions for random target generation, path time calculation, and optimal shoreline search.

### Phase 4: Build the UI
- Use Streamlit widgets for user controls:
  - a slider for shoreline X entry selection
  - a button to generate a new random target
- Render the pool, start point, target, chosen path, and optimal path using Matplotlib or Streamlit canvas.
- Display metrics for chosen path time and optimal path time.

### Phase 5: Validation and polish
- Verify the Streamlit app runs independently of the Pygame version.
- Confirm the UI matches the core behavior of the Pygame simulation.
- Add explanatory text and labels describing the water, land, and path colors.
- Handle initial state and reset behavior cleanly.

### Phase 6: Optional deployment guidance
- Document how to run the app locally:
  - `pip install -r requirements.txt`
  - `streamlit run streamlit_app.py`
- Optionally add notes about deployment options such as Streamlit Community Cloud or other hosting.

## File plan

- `streamlit_app.py` — Streamlit entrypoint and UI.
- `requirements.txt` — Streamlit dependencies.
- `STREAMLIT_IMPLEMENTATION_PLAN.md` — This implementation plan.
- `README.md` — Updated instructions describing both desktop and Streamlit usage.

## Notes

- This plan keeps the existing Pygame app intact.
- The Streamlit version will be added in parallel, not as a replacement.
