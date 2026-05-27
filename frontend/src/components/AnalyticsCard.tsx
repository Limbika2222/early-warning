interface AnalyticsCardProps {

    title: string;
    value: string | number;
    color: string;
  
  }
  
  export default function AnalyticsCard(
    { title, value, color }: AnalyticsCardProps
  ) {
  
    return (
  
      <div className={`bg-gradient-to-br ${color} text-white rounded-3xl p-8 shadow-lg`}>
  
        <p className="font-semibold opacity-80">
  
          {title}
  
        </p>
  
        <h2 className="text-6xl font-black mt-2">
  
          {value}
  
        </h2>
      </div>
    );
  }