'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function AppPage() {
  const [file, setFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const router = useRouter()

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0])
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (file) {
      setIsUploading(true)
      const formData = new FormData()
      formData.append('file', file)

      try {
        const response = await fetch('http://localhost:5000/api/upload', {
          method: 'POST',
          body: formData,
        })

        if (response.ok) {
          const result = await response.json()
          console.log('File uploaded successfully:', result)
          router.push('/results')
        } else {
          // router.push('/results')
          throw new Error('File upload failed')
        }
      } catch (error) {
        console.error('Error uploading file:', error)
        // 여기에 에러 처리 로직을 추가할 수 있습니다 (예: 사용자에게 에러 메시지 표시)
        // router.push('/results')
      } finally {
        setIsUploading(false)
      }
    }
  }

  return (
    <div className="container mx-auto mt-10">
      <Card className="w-full max-w-md mx-auto">
        <CardHeader>
          <CardTitle>채팅 기록 분석</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Input type="file" onChange={handleFileChange} accept=".txt" />
            </div>
            <Button type="submit" disabled={!file || isUploading}>
              {isUploading ? '업로드 중...' : '분석 시작'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}