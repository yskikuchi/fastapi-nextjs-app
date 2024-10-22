import BookingForm from '@/components/BookingForm';
import Calendar from '@/components/Calendar';

export default function Home() {
  return (
    <div>
      <div className="m-10 max-w-xl">
        <Calendar />
      </div>
      <div className="m-10">
        <BookingForm />
      </div>
    </div>
  );
}
