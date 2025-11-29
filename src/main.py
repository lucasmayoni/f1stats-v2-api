import fastf1
from fastf1 import plotting
from matplotlib import pyplot as plt
import os

# Enable caching
fastf1.Cache.enable_cache('data')

# Setup plotting
plotting.setup_mpl()

def main():
    # Ensure output directory exists
    os.makedirs('output', exist_ok=True)

    print("Loading session data...")
    # Load a session (2021 Bahrain Grand Prix, Qualifying)
    session = fastf1.get_session(2021, 'Bahrain', 'Q')
    session.load()

    print("Getting fastest lap...")
    # Get the fastest lap
    fastest_lap = session.laps.pick_fastest()
    car_data = fastest_lap.get_car_data().add_distance()
    
    print(f"Fastest Lap: {fastest_lap['Driver']} - {fastest_lap['LapTime']}")

    # Export to JSON
    json_output_file = 'output/fastest_lap_telemetry.json'
    print(f"Exporting telemetry to {json_output_file}...")
    # 'records' orientation is usually best for consumption by frontend apps (list of objects)
    car_data.to_json(json_output_file, orient='records')
    print("JSON export complete.")

    # Plot telemetry
    print("Plotting telemetry...")
    fig, ax = plt.subplots()
    ax.plot(car_data['Distance'], car_data['Speed'], label='Speed')
    ax.set_xlabel('Distance [m]')
    ax.set_ylabel('Speed [km/h]')
    ax.set_title(f"{session.event['EventName']} 2021 - {fastest_lap['Driver']} - Speed")
    ax.legend()
    
    # Save the plot
    output_file = 'output/fastest_lap_speed.png'
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    main()
