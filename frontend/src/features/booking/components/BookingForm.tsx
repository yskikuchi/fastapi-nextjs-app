'use client';

import { ChangeEvent, useEffect, useState } from 'react';
import DatePicker, { registerLocale } from 'react-datepicker';
import { ja } from 'date-fns/locale';
import { Car } from '@/types/Car';
import { postBooking } from '@/api/booking';
import { useRouter } from 'next/navigation';
import { getCars } from '@/api/car';

const jaLocale = {
  ...ja,
  options: { ...ja.options },
};

registerLocale('ja', jaLocale);

export default function BookingForm() {
  const router = useRouter();
  const [startTime, setStartTime] = useState<Date>(
    new Date(new Date().setHours(0, 0, 0, 0))
  );
  const [endTime, setEndTime] = useState<Date>(
    new Date(new Date().setHours(0, 0, 0, 0))
  );
  const [firstName, setFirstName] = useState<string>('');
  const [lastName, setLastName] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [selectedCar, setSelectedCar] = useState<Car | null>(null);
  const [totalAmount, setTotalAmount] = useState<number>(0);
  const [cars, setCars] = useState<Car[]>([]);

  useEffect(() => {
    const fetchCars = async () => {
      const response = await getCars();
      setCars(response);
      setSelectedCar(response[0]);
    };

    fetchCars();
  }, []);

  const calculateTotalPrice = (startTime: Date, endTime: Date) => {
    const priceForInitialTwelveHours = selectedCar?.priceForInitialTwelveHours;
    const pricePerAdditionalSixHours = selectedCar?.pricePerAdditionalSixHours;
    const diffInMSec = endTime.getTime() - startTime.getTime();
    const diffInHours = diffInMSec / 1000 / 60 / 60;

    if (!priceForInitialTwelveHours || !pricePerAdditionalSixHours) return;
    if (diffInMSec < 0) return;

    if (diffInHours <= 12) {
      setTotalAmount(priceForInitialTwelveHours);
    } else {
      const additionalHours = diffInHours - 12;
      const totalPrice =
        priceForInitialTwelveHours +
        Math.ceil(additionalHours / 6) * pricePerAdditionalSixHours;
      setTotalAmount(totalPrice);
    }
  };

  const handleLastNameChange = (e: ChangeEvent<HTMLInputElement>) => {
    setLastName(e.target.value);
  };

  const handleFirstNameChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFirstName(e.target.value);
  };

  const handleStartTimeChange = (date: Date) => {
    setStartTime(date);
    calculateTotalPrice(date, endTime);
  };

  const handleEndTimeChange = (date: Date) => {
    setEndTime(date);
    calculateTotalPrice(startTime, date);
  };

  const handleBook = async () => {
    const data = {
      carId: selectedCar?.id || '',
      startTime: startTime.toISOString().slice(0, -1),
      endTime: endTime.toISOString().slice(0, -1),
      amount: totalAmount,
      user: {
        name: `${lastName} ${firstName}`,
        email: email,
      },
    };

    const response = await postBooking(data);
    router.push(
      `/bookings/complete?referenceNumber=${response.referenceNumber}`
    );
  };

  return (
    <form className="w-full max-w-lg">
      <div className="flex flex-wrap -mx-3 mb-6">
        <div className="w-full md:w-1/2 px-3 mb-6 md:mb-0">
          <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2">
            車両
          </label>
          <select
            className="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
            onChange={(e) =>
              setSelectedCar(
                cars.find((car) => car.id === e.target.value) || null
              )
            }
          >
            {cars.map((car) => {
              return (
                <option key={car.id} value={car.id}>
                  {car.name}
                </option>
              );
            })}
          </select>
        </div>
      </div>
      <div className="flex flex-wrap -mx-3 mb-6">
        <div className="w-full md:w-1/2 px-3 mb-6 md:mb-0">
          <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2">
            利用開始日時
          </label>
          <DatePicker
            dateFormat="yyyy/MM/dd HH:mm"
            locale="ja"
            selected={startTime}
            showTimeSelect
            timeIntervals={30}
            onChange={(date) => handleStartTimeChange(date!)}
            className='appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"'
          />
        </div>
        <div className="w-full md:w-1/2 px-3 mb-6 md:mb-0">
          <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2">
            利用終了日時
          </label>
          <DatePicker
            dateFormat="yyyy/MM/dd HH:mm"
            locale="ja"
            selected={endTime}
            showTimeSelect
            timeIntervals={30}
            onChange={(date) => handleEndTimeChange(date!)}
            className='appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"'
          />
        </div>
        <div className="w-full md:w-1/2 px-3 mb-6 md:mb-0">
          <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2">
            氏
          </label>
          <input
            className="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
            type="text"
            value={lastName}
            onChange={handleLastNameChange}
          />
        </div>
        <div className="w-full md:w-1/2 px-3">
          <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2">
            名
          </label>
          <input
            className="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white"
            type="text"
            value={firstName}
            onChange={handleFirstNameChange}
          />
        </div>
      </div>
      <div className="flex flex-wrap -mx-3 mb-6">
        <div className="w-full px-3">
          <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2">
            E-mail
          </label>
          <input
            className="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder=""
          />
        </div>
      </div>
      <div className="flex flex-wrap -mx-3 mb-6">
        <p>合計価格: {totalAmount}</p>
      </div>
      <button
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        type="button"
        onClick={handleBook}
      >
        予約する
      </button>
    </form>
  );
}
