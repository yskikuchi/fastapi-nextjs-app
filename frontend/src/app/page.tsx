import Link from 'next/link';

export default function Page() {
  return (
    <div>
      <h1>トップページ</h1>
      <Link href="/bookings">予約画面へ</Link>
    </div>
  );
}
